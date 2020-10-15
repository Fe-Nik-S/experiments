#!/usr/bin/env python
# -*- coding: utf-8 -*-

# logging setup
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s - %(name)s - %(message)s")

logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

from operator import add
from collections import OrderedDict

# threading
from multiprocessing.pool import ThreadPool

# from multiprocessing.dummy import Pool as ThreadPool
from threading import Lock
import time
import datetime
import subprocess
import uuid
import os

# Zabbix api
from lib.metrics_utils import to_zabbix
import json
import requests
from lib import xmltodict, ntplib
from lib.utils import deep_getitem
from lib.pids_reference_base import ReferenceBase

# const
from lib.const import SENCORE_ATTRS_ENUM, SENCORE_DATA_PATH, SENCORE_URLS_ENUM, \
    TIMEOUT, TIME_SERVER, URL_REQUEST_TIMEOUT, \
    ZABBIX_HOST, ZABBIX_PORT, DATETIME_FORMAT, \
    TEMP_PATH, AUTODISCOVERY_SEND_PERIOD, AUTODISCOVERY_SEND_TIMESTAMP


class Sencore(object):
    def __init__(self, address, name, lock, reference_base):
        self.logger = logging.getLogger(name)
        self.address = address
        self.name = name
        self.lock = lock
        self.reference_base = reference_base
        self.data = {
            "tss": {},
            "qam": {}
        }
        self.session = requests.session()
        self.analyzer_type_handler = OrderedDict(
            is_regular=(   self.get_eth,
                           self.get_etr,
                           self.get_general,
                           self.get_status,
                           self.get_time_eth,
                           self.get_time_qam,
                        ),
            is_rgs=(self.get_etr_qam, self.get_tdt_time,),
            is_scr= (self.get_reference_compare, ),
            is_reciv = ()
        )

    @property
    def is_regular(self):
        """
        for all
        :return:
        """
        return True

    @property
    def is_reciv(self):
        """
        for resiv analyzers
        :return:
        """
        self.data["is_reciv"] = "reciv" in self.name.lower()
        return self.data["is_reciv"]

    @property
    def is_rgs(self):
        """
        for rgs analyzers
        :return:
        """
        self.data["is_rgs"] = "rgs" in self.name.lower()
        return self.data["is_rgs"]

    @property
    def is_scr(self):
        """
        for src analyzers
        :return:
        """
        self.data["is_scr"] = "scr" in self.name.lower()
        return self.data["is_scr"]

    def request(self, url, log=False, **kwargs):
        """

        :param url: url template
        :param kwargs: attrs for url build
        :return:
        """
        url = url.format(address=self.address, **kwargs or {})
        if log:
            self.logger.info(url)

        request = self.session.get(url, timeout=URL_REQUEST_TIMEOUT)
        if not request.text:
            return {}

        return xmltodict.parse(request.text.encode("utf-8"), attr_prefix='')

    def get_eth(self):
        """
        parse eth data from analyzer
        :return:
        """
        data_eth = self.request(SENCORE_URLS_ENUM.ETH)
        for ts_data in deep_getitem(data_eth, SENCORE_DATA_PATH.ETH_TSS.PATH):
            self.data["tss"][ts_data["name"]] = {
                attr: ts_data.get(attr) for attr in SENCORE_DATA_PATH.ETH_TSS.ATTR
            }
            self.data["tss"][ts_data["name"]]["services"] = {}

    def get_etr(self):
        """
        parse etr data
        :return:
        """
        for ts_name in self.data["tss"]:
            ts_data = self.data["tss"][ts_name]
            ts_index = ts_data["index"]
            data_ert = self.request(SENCORE_URLS_ENUM.ETR, input_id=100, ts_index=ts_index)
            pids_raw = deep_getitem(data_ert, SENCORE_DATA_PATH.ETR_PIDS.PATH)

            if not pids_raw:
                continue
            if not isinstance(pids_raw, list):
                pids_raw = [pids_raw]
            pids_ids = set([p["id"] for p in pids_raw])

            services_raw = deep_getitem(data_ert, SENCORE_DATA_PATH.ETR_SERVICES.PATH)

            if not services_raw:
                continue

            if isinstance(services_raw, dict):
                services = [services_raw]
            else:
                services = services_raw

            for service in services:
                pmt_pid = [p for p in service["pid"] if p["type"] == "PMT"][0]["id"]
                service_data = {
                    attr: service.get(attr) for attr in SENCORE_DATA_PATH.ETR_SERVICES.ATTR
                }
                service_data["service_pids"] = [
                    p.get("id") for p in service["pid"]
                ]
                service_data["not_existed"] = []
                service_data["id"] = service.get("id")
                service_data["pids"] = {}
                for pid_raw in pids_raw:
                    pid_id = pid_raw["id"]
                    if pid_id in service_data.get("service_pids", {}):
                        pid_data = {
                            attr[0] if isinstance(attr, tuple) else attr:
                                pid_raw.get(attr[1] if isinstance(attr, tuple) else attr)
                            for attr in SENCORE_DATA_PATH.ETR_PIDS.ATTR
                        }
                        service_data["pids"][pid_data["id"]] = pid_data

                service_data["scrambled"] = any(map(lambda x: x["scrambled"], service_data["pids"].values()))

                for pid in SENCORE_ATTRS_ENUM.REQUIRED_PIDS:
                    if pid not in pids_ids:
                        service_data["not_existed"].append(pid)
                ts_data["services"][service_data["id"]] = service_data
                ts_data["services"]["count"] = len(services_raw)
            pid_empty = set(service_data["not_existed"])
            ts_data["not_existed"] = ",".join(pid_empty) if pid_empty else "OK"

            ts_data["scrambled"] = any(map(lambda x: x["scrambled"],
                                           [v for v in ts_data["services"].values() if not isinstance(v, int)]))

            ts_checks = {}
            ts_checks_raw = deep_getitem(data_ert, SENCORE_DATA_PATH.ETR_CHECKS.PATH)
            if not ts_checks_raw:
                continue

            for check_p in ts_checks_raw:
                priority_name = "_".join(
                    check_p["name"].replace(".", "").split(" ")
                ).lower()

                ts_checks[priority_name] = {}

                for check in check_p["check"]:
                    if not isinstance(check, dict):
                        continue
                    check_name = "_".join(check["name"].split(" ")).lower()
                    ts_checks[priority_name][check_name] = check.get("currentErrorCount")
                ts_checks[priority_name]["count"] = sum(map(lambda x: int(x), ts_checks[priority_name].values()))
            ts_data["checks"] = ts_checks

    def get_general(self):
        data_general = self.request(SENCORE_URLS_ENUM.GENERAL)
        self.data[SENCORE_DATA_PATH.GENERAL_VERSION.ATTR] = deep_getitem(
            data_general, SENCORE_DATA_PATH.GENERAL_VERSION.PATH)

        self.data[SENCORE_DATA_PATH.GENERAL_UPTIME.ATTR] = deep_getitem(
            data_general, SENCORE_DATA_PATH.GENERAL_UPTIME.PATH)

        mlerr_table = deep_getitem(data_general, SENCORE_DATA_PATH.GENERAL_MLERROR.PATH)
        mw_table = deep_getitem(data_general, SENCORE_DATA_PATH.GENERAL_MW.PATH)
        channel_table = deep_getitem(data_general, SENCORE_DATA_PATH.GENERAL_CHANNEL.PATH)

        for ts_name in self.data["tss"]:
            ts_nm = self.data["tss"][ts_name]["name"]
            for channel in channel_table:
                if ts_nm == channel["name"]:
                    channel_data = {
                        attr[0] if isinstance(attr, tuple) else attr:
                            channel.get(attr[1] if isinstance(attr, tuple) else attr)
                        for attr in SENCORE_DATA_PATH.GENERAL_CHANNEL.ATTR
                    }
                    self.data["tss"][ts_name].update(channel_data)
                    break

            ts_index = self.data["tss"][ts_name]["chindex"]

            for mlerr in mlerr_table:
                if ts_index == mlerr["chindex"]:
                    mlerr_data = {
                        attr[0] if isinstance(attr, tuple) else attr:
                            mlerr.get(attr[1] if isinstance(attr, tuple) else attr)
                        for attr in SENCORE_DATA_PATH.GENERAL_MLERROR.ATTR
                    }
                    self.data["tss"][ts_name].update(mlerr_data)
                    break

            for mwerr in mw_table:
                if ts_index == mwerr["chindex"]:
                    mwerr_data = {
                        attr[0] if isinstance(attr, tuple) else attr:
                            mwerr.get(attr[1] if isinstance(attr, tuple) else attr)
                        for attr in SENCORE_DATA_PATH.GENERAL_MW.ATTR
                    }
                    self.data["tss"][ts_name].update(mwerr_data)
                    break

    def get_status(self):
        data_status = self.request(SENCORE_URLS_ENUM.STATUS)

        for item in (SENCORE_DATA_PATH.STATUS_CPU_TEMP, SENCORE_DATA_PATH.STATUS_CPU_TEMP,
                     SENCORE_DATA_PATH.STATUS_FREE_MEM, SENCORE_DATA_PATH.STATUS_FREE_DISC, SENCORE_DATA_PATH.STATUS_TIME):
            self.data[item.ATTR] = deep_getitem(data_status, item.PATH)

        port_info = deep_getitem(data_status, SENCORE_DATA_PATH.STATUS_PORT)

        port_info = port_info.split(" ") if port_info else ("NO_DATA", "NO_DATA")
        port, bitrate = port_info[0], port_info[-1]
        if bitrate != "NO_DATA":
            bitrate = ''.join([x for x in bitrate if x.isdigit() or x == '.'])
            bitrate = int(round((float(bitrate))))
        self.data["port"] = port
        self.data["bitrate"] = unicode(bitrate)

    def get_reference_compare(self):
        with self.lock:
            self.reference_base.check(self.data["tss"])

    def get_etr_qam(self):
        qam_data = self.data["qam"]
        qam_data["tss"] = {}
        qam_data_tss = qam_data["tss"]
        data_ert_qam = self.request(SENCORE_URLS_ENUM.ETR_ALL)
        ert_inputs = deep_getitem(data_ert_qam, SENCORE_DATA_PATH.ETR_INPUTS.PATH)
        ert_qam_inputs = [inp for inp in ert_inputs if inp["name"] == "QAM1"]
        if not ert_qam_inputs:
            return
        ert_qam_input = ert_qam_inputs[0]
        ert_qam_input_id = ert_qam_input.get("id")
        for ts_data in ert_qam_input["tuningSetup"]:
            qam_data_tss[ts_data["name"]] = {
                attr[0] if isinstance(attr, tuple) else attr:
                    ts_data.get(attr[1] if isinstance(attr, tuple) else attr)
                for attr in SENCORE_DATA_PATH.ETR_INPUTS.ATTR
            }
            qam_data_tss[ts_data["name"]]["services"] = {}
            services_raw = self.request(
                SENCORE_URLS_ENUM.ETR, input_id=ert_qam_input_id, ts_index=ts_data.get("id"))
            services = deep_getitem(services_raw, SENCORE_DATA_PATH.ETR_SERVICES.PATH)
            if not services:
                continue
            qam_data_tss_services = qam_data_tss[ts_data["name"]]["services"]
            for service in services:
                qam_data_tss_services[service["id"]] = {}
                qam_data_tss_services[service["id"]] = {
                    attr[0] if isinstance(attr, tuple) else attr:
                        ts_data.get(attr[1] if isinstance(attr, tuple) else attr)
                    for attr in SENCORE_DATA_PATH.GENERAL_MW.ATTR
                }
                qam_data_tss_services[service["id"]]["pid_count"] = len(service["pid"])
            check = [o for o in deep_getitem(
                services_raw,
                SENCORE_DATA_PATH.ETR_CHECKS.PATH
            ) if o["name"] == "Interface checks"][0]

            qam_data_tss[ts_data["name"]]["sid_count"] = len(qam_data_tss[ts_data["name"]]["services"])

    def get_tdt_time(self):
        tdt_time_data = self.request(SENCORE_URLS_ENUM.TDT_TIME)
        tdt_time_datas = deep_getitem(tdt_time_data, "tree,item")
        if tdt_time_datas:
            item = [o for o in tdt_time_datas if o["id"] == "H_d_d_d_p20_t112_s0_x-1_a0_s24_e63_l1"][0]
            self.data["date"] = item["value"]

    def get_time_qam(self):
        qam_time_data = self.request(SENCORE_URLS_ENUM.QAM_TIME)
        qam_time_datas = deep_getitem(qam_time_data, "tree,item")
        self.data["time_qam"] = 0
        if qam_time_datas:
            item = [o for o in qam_time_datas if o["id"] == "H_d_d_d_p20_t112_s0_x-1_a0_s24_e63_l1"][0]
            epoch = datetime.datetime(1970, 1, 1)
            ntp_client = ntplib.NTPClient()
            ntp_time = ntp_client.request(TIME_SERVER).tx_time
            dt = datetime.datetime.strptime(item["value"], "%Y.%m.%d %H:%M:%S")
            current_time = int((dt - epoch).total_seconds())
            self.data["time_qam"] = current_time
            self.data["time_qam_diff"] = current_time - ntp_time

    def get_time_eth(self):
        eth_time_data = self.request(SENCORE_URLS_ENUM.ETH_TIME)
        eth_time_datas = deep_getitem(eth_time_data, "tree,item")
        self.data["time_eth"] = 0
        if eth_time_datas:
            item = [o for o in eth_time_datas if o["id"] == "H_d_d_d_p20_t112_s0_x-1_a0_s24_e63_l1"][0]
            epoch = datetime.datetime(1970, 1, 1)
            ntp_client = ntplib.NTPClient()
            ntp_time = ntp_client.request(TIME_SERVER).tx_time
            dt = datetime.datetime.strptime(item["value"], "%Y.%m.%d %H:%M:%S")
            current_time = int((dt - epoch).total_seconds())
            self.data["time_eth"] = current_time
            self.data["time_eth_diff"] = current_time - ntp_time

    def get_all(self):
        kwargs = {}

        for th in self.analyzer_type_handler:
            kwargs[th] = getattr(self, th)
            if not kwargs[th]:
                continue
            for func in self.analyzer_type_handler[th]:
                try:
                    func()
                except Exception as why:
                    self.logger.exception(why)

        return self.name, self.data

def sencore_start(args):
    sencore = Sencore(args[0], args[1], args[2], args[3])
    return sencore.get_all()

def get_hosts():
    hosts = [        
    ]

    analyzers = {}

    for host in hosts:
        analyzers[host[0]] = {
            'ip': host[0],
            'host': host[1]
        }

    return analyzers

def jdumps(o):
    return json.dumps(o, ensure_ascii=False)

def write_metrics2file(metrics, file):
    with open(file, 'wb') as send_data:
        for item in metrics:
            send_data.write(' '.join([jdumps(item[0]), jdumps(item[1]), jdumps(item[2]), '\n']))
        send_data.close()


def need_send_autodiscovery():
    result = True

    try:
        with open(''.join([TEMP_PATH, AUTODISCOVERY_SEND_TIMESTAMP])) as file:
            data = file.read()

        last_send_datetime = datetime.datetime.strptime(data, DATETIME_FORMAT)
        delta = datetime.timedelta(hours=AUTODISCOVERY_SEND_PERIOD)
        next_run = last_send_datetime + delta

        result = next_run < datetime.datetime.now()
    except Exception:
        pass
    return result


def send2zabbix(file):
    cmd = 'zabbix_sender -z %s -p %s -i %s'%\
            (ZABBIX_HOST, ZABBIX_PORT, file)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p.communicate()


def write_last_send_timestamp():
    try:
        with open(''.join([TEMP_PATH, AUTODISCOVERY_SEND_TIMESTAMP]), 'wb') as file:
            file.write(datetime.datetime.now().strftime(DATETIME_FORMAT))
        file.close()
    except Exception:
        pass


if __name__ == "__main__":
    tim_start = time.time()

    # reference base for pids and scrambled status
    rb = ReferenceBase(SENCORE_URLS_ENUM.REFERENCE_BASE_URL)

    # lock for reference base
    lock = Lock()

    # get hosts from zabbix
    analyzers = get_hosts()
    # prepare data for thread pool
    data_to_process = [(a["ip"], a["host"], lock, rb) for a in analyzers.values() if a.get("ip", None)]

    # init thread pool
    sencore_pool = ThreadPool(
        processes=len(data_to_process)
    ).map_async(sencore_start, data_to_process)

    # wait until all threads done
    counter = 0
    while not sencore_pool.ready() and counter < TIMEOUT:
        time.sleep(0.1)
        counter += 0.1
    if counter >= TIMEOUT:
        exit(1)

    # get results from thread pool
    data = sencore_pool.get()

    # # generate Zabbix metrics
    zabbix_metrics_all = [to_zabbix(d[0], d[1]) for d in data if d]

    # autodiscovery metrics
    zabbix_metrics_discovery = reduce(add, [zma["autodiscovery"] for zma in zabbix_metrics_all])
    zabbix_metrics_discovery = sorted(zabbix_metrics_discovery, key=lambda x: x[0])

    # static metrics
    zabbix_metrics_static = reduce(add, [zma["static"] for zma in zabbix_metrics_all])

    # dynamic metrics
    zabbix_metrics_dynamic = reduce(add, [zma["dynamic"] for zma in zabbix_metrics_all])

    send2zabbix_metrics = zabbix_metrics_static
    send2zabbix_metrics += zabbix_metrics_dynamic
    send2zabbix_metrics = sorted(send2zabbix_metrics, key=lambda x: x[0])

    uid = str(uuid.uuid4())
    discovery_data_file = ''.join([TEMP_PATH, 'discovery_', uid])
    metrics_data_file = ''.join([TEMP_PATH, 'metrics_', uid])

    write_metrics2file(zabbix_metrics_discovery, discovery_data_file)
    write_metrics2file(send2zabbix_metrics, metrics_data_file)

    if need_send_autodiscovery():
        send2zabbix(discovery_data_file)
        write_last_send_timestamp()

    send2zabbix(metrics_data_file)
