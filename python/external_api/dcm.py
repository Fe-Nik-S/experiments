# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import struct
import socket
import time
import os
import datetime
import logging
from operator import add

logging.basicConfig(level=logging.INFO)

library_paths = (
    "/usr/lib/python2.2/site-packages/omniORBpy",
    "/app/gui/embgui/libs/giop/stubs",
    "/app/gui/embgui/libs",
    "/app/gui/site-packages"
)
sys.path.extend(library_paths)

from omniORB import CORBA
import DCM
from json import (dumps as jdumps,
                  loads as jloads)

TIMESTAP_FILE = '/tmp/timestamp'
AUTODISCOVERY_SEND_PERIOD = 5
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

SEND_METRICS_COUNT = 250

ORB_IOR = ("IOR:010000001a00000049444c3a44434d2f446576696"
           "365436f6e74726f6c3a312e3000000001000000000000"
           "005c0000000101020009000000677569626f617264000"
           "0ec130c0000004c6a46f3000015470000000102000000"
           "00000000080000000100000000545441010000001c000"
           "000010000000100010001000000010001050901010001"
           "00000009010100")

TEMPERATURE = (
    ("left", "2c", "2"),
    ("right", "2d", "2"),
    ("CPU", "2c", "1"),
    ("coproc_CPU", "2d", "1")
)

VOLTAGE = (
    ("FPGA", "14", "in1_input"),
    ("CN63", "14", "in2_input"),
    ("COPROC", "14", "in3_input"),
    ("1V2", "14", "in4_input"),
    ("1V8", "14", "in5_input"),
    ("2V5", "14", "in6_input"),
    ("3V3", "14", "in8_input"),
    ("12-3", "14", "in9_input"),
    ("1V5", "14", "in10_input"),
    ("PGOOD", "14", "in12_input")
)

ZBX_MESSAGE_TEMPLATE = ("\t\t{\n"
                        "\t\t\t\"host\":%s,\n"
                        "\t\t\t\"key\":%s,\n"
                        "\t\t\t\"value\":%s,\n"
                        "\t\t\t\"clock\":%s}")

ZBX_REQUEST_TEMPLATE = ("{\n"
                        "\t\"request\":\"sender data\",\n"
                        "\t\"data\":[\n%s]\n"
                        "}")

def send_to_zabbix(metrics, zabbix_host="", zabbix_port=10051):
    """Send set of metrics to Zabbix server."""

    def _recv_all(sock, count):
        buf = []
        while len(buf) < count:
            chunk = sock.recv(count - len(buf))
            if not chunk:
                return buf
            buf.extend(chunk)
        return "".join(buf)

    metrics_data = []
    for m in metrics:
        metrics_data.append(ZBX_MESSAGE_TEMPLATE % (jdumps(m[0]), jdumps(m[1]), jdumps(m[2]), int(time.time())))
    json_data = ZBX_REQUEST_TEMPLATE % (",\n".join(metrics_data))
    data_len = struct.pack("<Q", len(json_data))
    packet = "ZBXD\1" + data_len + json_data
    zabbix = socket.socket()
    zabbix.connect((zabbix_host, zabbix_port))
    zabbix.sendall(packet)
    resp_hdr = _recv_all(zabbix, 13)
    if not resp_hdr.startswith("ZBXD\1") or len(resp_hdr) != 13:
        return False
    resp_body_len = struct.unpack("<Q", resp_hdr[5:])[0]
    resp_body = zabbix.recv(resp_body_len)
    zabbix.close()
    resp = jloads(resp_body)
    print resp
    if (resp.get("response") != "success") \
            or (resp.get("failed") != 0):
        return False
    return True

def deep_getattr(obj, attr):
    return reduce(getattr, attr.split('.'), obj)

class Dcm(object):
    def __init__(self, host='localhost', port=9000, trace_level=0, timeout=0):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("init")
        self.orb_conn = CORBA.ORB_init(
            ["-ORBendPoint", "giop:tcp:%s:%d" % (host, port),
             "-ORBmaxGIOPVersion", "1.1",
             "-ORBverifyObjectExistsAndType", "0",
             "-ORBstrictIIOP", "0",
             "-ORBclientCallTimeOutPeriod", "%d" % timeout,
             "-ORBoutConScanPeriod", "0",
             "-ORBscanGranularity", "0",
             "-ORBgiopMaxMsgSize", "60000000",
             "-ORBtraceLevel", "%d" % trace_level],
            CORBA.ORB_ID)

        self.conn = self.orb_conn.string_to_object(
            self.get_ior())
        self.logon()

    def __del__(self):
        self.logger.info("disconnect")
        self.logout()

    def logon(self):
        self.logger.info("connect")
        self.conn.LogOn(
            DCM.DeviceControl.Client_Gui,
            "guest", "guest", "guest")

    def logout(self):
        self.conn.LogOff("guest")

    @property
    def uptime(self):
        return self.conn.GetUptime()

    def get_ior(self):
        return ORB_IOR

    @classmethod
    def resolve_device(cls, address):
        for hwmon in os.listdir("/sys/class/hwmon"):
            path = os.path.join("/sys/class/hwmon", hwmon, "device")
            device = os.path.basename(os.readlink(path))
            if device.endswith(address):
                return path
        return None

    def get_temperature(self, address, tempid):
        path = os.path.join(self.resolve_device(address),
                            "temp%s_input" % tempid)
        if not os.path.exists(path):
            return 0
        with open(path, "r") as out:
            return float(out.read()) / 1000

    def get_voltage(self, address, voltid):
        path = os.path.join(self.resolve_device(address), voltid)
        if not os.path.exists(path):
            return 0
        with open(path, "r") as out:
            return float(out.read()) / 1000

    @property
    def temperatures(self):
        return dict((name, self.get_temperature(address, id))
                    for name, address, id in TEMPERATURE)

    @property
    def voltages(self):
        return dict((name, self.get_voltage(address, id))
                    for name, address, id in VOLTAGE)

    @property
    def boards(self):
        for board in self.conn.BoardGetL_V2():
            yield Board(conn=self.conn, obj=board)

    @property
    def in_board(self):
        for board in self.boards:
            if board.is_input:
                return board

    @property
    def out_board(self):
        for board in self.boards:
            if not board.is_input:
                return board


class Board(object):
    def __init__(self, conn, obj):
        self.conn = conn
        self.obj = obj
        self.logger = logging.getLogger(repr(self))
        self.phys_ref = DCM.DeviceControl.IPS_Ref_t(
            BoardNr=self.obj.BoardNumber, PortNr=0)
        self.logger.debug("init")

    @property
    def is_input(self):
        if str(self.obj.BoardType).endswith("IN"):
            return True
        else:
            return False

    def get_ts(self, sids=None):
        if self.is_input:
            for ts in self.conn.IPS_InTS_GetL(
                    self.phys_ref, sids or []):
                yield TS(conn=self.conn, obj=ts, parent=self)
        else:
            for ts in self.conn.IPS_OutTS_GetL(
                    self.phys_ref, sids or []):
                yield TS(conn=self.conn, obj=ts, parent=self)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__,
                             str(self.obj.BoardType))


class TS(object):
    def __init__(self, conn, obj, parent):
        self.conn = conn
        self.obj = obj
        self.parent = parent
        self.logger = logging.getLogger(repr(self))
        self.logger.debug("init")

    @property
    def is_input(self):
        return isinstance(self.obj, DCM.DeviceControl.IPS_InputTS_t)

    @property
    def mcast_address(self):
        return self.obj.Socket.IP

    @property
    def bitrate(self):
        bitrate_all = self.conn.MM_GetOutputTS_BitRate(self.obj.Ref)
        return bitrate_all[0].TotalRate.CurBitRate

    def get_services(self, sid_list=None):
        if self.is_input:
            for service in self.conn.IPS_InServiceGetL(
                    self.obj.RefIn, sid_list or []):
                yield Service(conn=self.conn, obj=service, parent=self)
        else:
            for service in self.conn.IPS_OutServiceGetL(
                    self.obj.Ref, sid_list or []):
                yield Service(conn=self.conn, obj=service, parent=self)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, str(self.obj.Socket.IP))


class Service(object):
    def __init__(self, conn, obj, parent):
        self.conn = conn
        self.obj = obj
        self.parent = parent
        self.logger = logging.getLogger(repr(self))
        self.logger.debug("init")

    @property
    def is_input(self):
        return isinstance(
            self.obj,
            DCM.DeviceControl.IPS_Service_In_t)

    @property
    def is_scrambled(self):
        return (self.obj.ServiceInProperty == 25L)

    @property
    def name(self):
        if self.is_input:
            channnel_name = "%s_%s" % (
                self.obj.InputSID,
                self.obj.UserName.strip())
            return transliterate(channnel_name).upper().decode('unicode_escape').encode('utf-8')
        else:
            channnel_name = "%s_%s" % (
                self.obj.OutputSID,
                self.obj.SDTData.OutputUserName.strip())
            return transliterate(channnel_name).upper().decode('unicode_escape').encode('utf-8')

    @property
    def sid(self):
        if self.is_input:
            return self.obj.InputSID
        else:
            return self.obj.OutputSID

    @property
    def backup_sources(self):
        sources = self.conn.GetServiceBU_BackupL_V2(
            DCM.DeviceControl.IPS_Service_t(
                self.obj.RefOut,
                self.obj.OutputSID), [])
        return [source.BackupService for source in sources[0].BackupSrvTableList[0].BackupSvcList]

    @property
    def main_source(self):
        try:
            return self.conn.IPS_OutServiceGetL_V2(self.obj.RefOut,\
                                                   [self.obj.OutputSID])[0].MainInputService.Service
        except AttributeError:
            return None

    @property
    def sources(self):
        backup_svc = [self.main_source]
        backup_svc.extend(self.backup_sources)
        return backup_svc

    @property
    def active_source_number(self):
        active_services = self.conn.GetActiveInputServices_V2(
            DCM.DeviceControl.IPS_Service_t(
                self.obj.RefOut,
                self.obj.OutputSID), [])
        active_service = active_services[0].ActiveInService
        for i, backup_service in enumerate(self.backup_sources, start=1):
            if active_service.SID == backup_service.SID:
                return i
        return 0

    @property
    def components(self):
        if self.is_input:
            for component in self.conn.MM_GetInputSvcComponentBitRate(
                    self.obj.RefIn, [self.sid]):
                yield Component(conn=self.conn, obj=component, parent=self)
        else:
            for component in self.conn.MM_GetOutputSvcComponentBitRate(
                    self.obj.RefOut, [self.sid]):
                yield Component(conn=self.conn, obj=component, parent=self)

    def get_service_by_sid(self, find_svc):
        svc = self.conn.IPS_InServiceGetL(
                    find_svc.Ref, [find_svc.SID])[0]
        return Service(self.conn, svc, None) if svc else None

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, str(self.sid))


class Component(object):
    def __init__(self, conn, obj, parent):
        self.conn = conn
        self.obj = obj
        self.parent = parent
        self.logger = logging.getLogger(repr(self))
        self.logger.debug("init")

    @property
    def is_audio(self):
        return "audio" in self.obj.strEsType

    @property
    def is_video(self):
        return "video" in self.obj.strEsType

    @property
    def is_scrambled(self):
        return None

    @property
    def pid(self):
        return self.obj.PID

    @property
    def bitrate_current(self):
        return self.obj.Rate.CurBitRate

    @property
    def bitrate_avg(self):
        return self.obj.Rate.CurBitRate

    @property
    def bitrate_min(self):
        return self.obj.Rate.CurBitRate

    @property
    def bitrate_max(self):
        return self.obj.Rate.CurBitRate

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, str(self.pid))


def transliterate(name):
    to_replace = {'Ð¶': 'zh', 'Ð¾': 'o', 'Ð¿': 'p', 'Ð°': 'a', 'Ð±': 'b', 'Ð²': 'v',
                  'Ð³': 'g', 'Ð´': 'd', 'Ðµ': 'e', 'Ñ‘': 'e', 'Ð·': 'z', 'Ð¸': 'i',
                  'Ð¹': 'i', 'Ðº': 'k', 'Ð»': 'l', 'Ð¼': 'm', 'Ð½': 'n', 'Ñ€': 'r',
                  'Ñ': 's', 'Ñ‚': 't', 'Ñƒ': 'u', 'Ñ„': 'f', 'Ñ…': 'h', 'Ñ†': 'c',
                  'Ñ‡': 'cz', 'Ñˆ': 'sh', 'Ñ‰': 'scz', 'ÑŠ': '', 'Ñ‹': 'y', 'ÑŒ': '',
                  'Ñ': 'e', 'ÑŽ': 'u', 'Ñ': 'ja', 'Ð': 'a', 'Ð‘': 'b', 'Ð’': 'v',
                  'Ð“': 'g', 'Ð”': 'd', 'Ð•': 'e', 'Ð': 'e', 'Ð–': 'zh', 'Ð—': 'z',
                  'Ð˜': 'i', 'Ð™': 'i', 'Ðš': 'k', 'Ð›': 'l', 'Ðœ': 'm', 'Ð': 'n',
                  'Ðž': 'o', 'ÐŸ': 'p', 'Ð ': 'r', 'Ð¡': 's', 'Ð¢': 't', 'Ð£': 'u',
                  'Ð¤': 'Ð¥', 'Ð¦': 'c', 'Ð§': 'cz', 'Ð¨': 'sh', 'Ð©': 'scz', 'Ðª': '',
                  'Ð«': 'y', 'Ð¬': '', 'Ð­': 'e', 'Ð®': 'u', 'Ð¯': 'ja', ',': '',
                  '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '', '$': '',
                  '%': '', '^': '', '&': '', '*': '', '(': '', ')': '',
                  '=': '', '+': '', ':': '', ';': '', '<': '', '>': '', '\'': '',
                  '"': '', '\\': '', '/': '', 'â„–': '', '[': '', ']': '', '{': '',
                  '}': '', 'Ò‘': '', 'Ñ—': '', 'Ñ”': '', 'Ò': 'g', 'Ð‡': 'i', 'Ð„': 'e',
                  u'\x01': '', u'\x05': '', u'\x15': ''}

    for key in to_replace:
        try:
            name = name.replace(unicode(key), to_replace[key])
        except:
            try:
                name = name.replace(key, to_replace[key])
            except:
                pass
    return name

def need_send_autodiscovery():
    result = True

    try:
        with open(TIMESTAP_FILE) as file:
            data = file.read()

        last_send_datetime = datetime.datetime.strptime(data, DATETIME_FORMAT)
        delta = datetime.timedelta(hours=AUTODISCOVERY_SEND_PERIOD)
        next_run = last_send_datetime + delta

        result = next_run < datetime.datetime.now()
    except Exception:
        pass
    return result


def write_last_send_timestamp():
    try:
        with open(TIMESTAP_FILE, 'wb') as file:
            file.write(datetime.datetime.now().strftime(DATETIME_FORMAT))
        file.close()
    except Exception:
        pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit()

    host = sys.argv[1]
    dcm = Dcm()

    zabbix_data = []

    zabbix_data += [[host, "sys_uptime", int(dcm.uptime)]]
    temperatures = dcm.temperatures
    voltages = dcm.voltages

    for temperature in temperatures:
        zabbix_data += [[host, 'temperature_%s' % temperature, temperatures[temperature]]]

    for voltage in voltages:
        zabbix_data += [[host, 'voltage_%s' % voltage, voltages[voltage]]]

    in_board = dcm.in_board
    out_board = dcm.out_board

    # get ts's from in board
    tss_services_in = dict((ts, [service for service in ts.get_services()])
                           for ts in in_board.get_ts())

    # get ts's from output board
    tss_services_out = dict((ts, [service for service in ts.get_services()])
                            for ts in out_board.get_ts())

    # get services from output ts's
    all_svc_out = reduce(add, [service for service in tss_services_out.values()])
    all_svc_in = reduce(add, [service for service in tss_services_in.values()])

    zabbix_data += [[host, "countsrvin", len(all_svc_in)]]
    zabbix_data += [[host, "countsrvout", len(all_svc_out)]]

    if need_send_autodiscovery():
        # service name autodiscovery
        zabbix_data += [[host, 'channels_discovery_dcm',
                         jdumps({"data": [{"{#DCM_CHANNELS}": service.name} for service in all_svc_out]},
                                ensure_ascii=False)]]
        write_last_send_timestamp()

    # count of sources for service
    for svc in all_svc_out:
        zabbix_data += [[host, "count_in[{name}]".format(name=svc.name), len(svc.sources)]]

    # service states (active source number)
    for svc in all_svc_out:
        zabbix_data += [[host, "state[{name}]".format(name=svc.name), svc.active_source_number]]

    # is service scrembled and service bitrate
    for svc in all_svc_out:
        for num, _svc in enumerate([svc.get_service_by_sid(backup_svc) for backup_svc in svc.sources]):
            zabbix_data += [[host, "scrembler_{num}[{name}]".format(name=svc.name, num=num), 1 if (_svc and _svc.is_scrambled) else 0]]
            zabbix_data += [[host, "bitrate_in_{num}[{name}]".format(name=svc.name, num=num),
                             sum([c.bitrate_current for c in _svc.components])]]

    # service mcast number
    for svc in all_svc_out:
        zabbix_data += [[host, "mcast_out[{name}]".format(name=svc.name), svc.parent.mcast_address]]

    # all service pids
    all_svc_out_components = dict((service, [c for c in service.components]) for service in all_svc_out)

    # service video pid bitrate
    for svc in all_svc_out_components:
        video_component = filter(lambda x: x.is_video, [c for c in all_svc_out_components[svc]])
        zabbix_data += [[host, "bitrate_out_video[{name}]".format(name=svc.name),
                         video_component[0].bitrate_current if video_component else 0]]

    # service all pids bitrate
    for svc in all_svc_out_components:
        zabbix_data += [[host, "bitrate_out[{name}]".format(name=svc.name),
                         sum([c.bitrate_current for c in all_svc_out_components[svc]])]]

    while zabbix_data:
        send_to_zabbix(zabbix_data[:SEND_METRICS_COUNT])
        zabbix_data = zabbix_data[SEND_METRICS_COUNT:]
