#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

path_attr = namedtuple("path_attr", ("PATH", "ATTR"))

__ALL__ = ["SENCORE_URLS_ENUM", "SENCORE_DATA_PATH", "SENCORE_ATTRS_ENUM", "RESULT_PATH"]


class SENCORE_URLS_ENUM(object):
    ETH = "http://{address}/probe/ethdata"
    ETR_ALL = "http://{address}/probe/etrdata?&&"
    ETR = "http://{address}/probe/etrdata?inputId={input_id}&tuningSetupId={ts_index}"
    GENERAL = "http://{address}/probe/generaldata?&&"
    STATUS = "http://{address}/probe/status"
    REFERENCE_BASE_URL = "https://mgmt.hq.ertelecom.ru/chtp/api/dir/%7B%22rec_type_id%22:2020%7D"
    TDT_TIME = "http://{address}/probe/data/AnaParseTable?inputId=1&etrEngineNo=0&pid=0&tid=112&tidExtension=-1"
    QAM_TIME = "http://{address}/probe/data/AnaParseTable?inputId=1&etrEngineNo=0&pid=20&tid=112&tidExtension=-1"
    ETH_TIME = "http://{address}/probe/data/AnaParseTable?inputId=100&etrEngineNo=0&pid=20&tid=112&tidExtension=-1"


class SENCORE_ATTRS_ENUM(object):
    __slots__ = ("ETH", "REQUIRED_PIDS")
    ETH = ("bitrate", "name", "index", "cc_errors", "net_bitrate", "iat_avg")
    REQUIRED_PIDS = {"0", "1", "16", "17", "18", "20", "89", "99"}


class SENCORE_DATA_PATH(object):
    __slots__ = (
        "ETH_TSS", "ETR_PIDS", "ETR_PIDS", "ETR_SERVICES", "ETR_CHECKS",
        "GENERAL_VERSION", "GENERAL_MLERROR", "GENERAL_UPTIME",
        "STATUS_CPU_TEMP", "STATUS_PORT", "STATUS_FREE_DISC",
        "STATUS_STATUS_FREE_MEM", "STATUS_TIME"
    )

    ETH_TSS = path_attr(**{
        "PATH": "EthExportData,streams,mon",
        "ATTR": ("bitrate", "name", "index", "cc_errors",
                 "net_bitrate", "iat_avg", "dst_addr")
    })

    ETR_PIDS = path_attr(**{
        "PATH": "Etr290ExportData,input,tuningSetup,pidList,pid",
        "ATTR": ("id", "bitrate", ("max_bitrate", "maxBitrate"),
                 ("min_bitrate", "minBitrate"), ("num_cc_errors", "numCcErrors"), "scrambled")
    })

    ETR_SERVICES = path_attr(**{
        "PATH": "Etr290ExportData,input,tuningSetup,serviceList,service",
        "ATTR": ("id", "name", "bitrate", "scrambled", "symbolrate")
    })

    ETR_CHECKS = path_attr(**{
        "PATH": "Etr290ExportData,input,tuningSetup,etrList,group",
        "ATTR": ()
    })

    GENERAL_VERSION = path_attr(**{
        "PATH": "GeneralProbeExportData,release",
        "ATTR": "version"
    })

    GENERAL_UPTIME = path_attr(**{
        "PATH": "GeneralProbeExportData,internet,mgmt,mib2,system,sysUpTime",
        "ATTR": "uptime"
    })

    GENERAL_MLERROR = path_attr(**{
        "PATH": ("GeneralProbeExportData,internet,private,"
                 "enterprise,bridgetech,mlrerrTable,row"),
        "ATTR": ("mlrerr1m", )
    })

    GENERAL_MW = path_attr(**{
        "PATH": ("GeneralProbeExportData,internet,private,"
                 "enterprise,bridgetech,mwTable,row"),
        "ATTR": ("iatPeak1m", "mlrSum1m")
    })

    GENERAL_CHANNEL = path_attr(**{
        "PATH": ("GeneralProbeExportData,internet,private,"
                 "enterprise,bridgetech,channelTable,row"),
        "ATTR": ("chindex", )
    })

    STATUS_TIME = path_attr(**{
        "PATH": "Status,System,time",
        "ATTR": "time"
    })

    STATUS_CPU_TEMP = path_attr(**{
        "PATH": "Status,System,cpu_temp",
        "ATTR": "cpu_temp"
    })

    STATUS_FREE_MEM = path_attr(**{
        "PATH": "Status,Resources,ram_free",
        "ATTR": "free_mem"
    })

    STATUS_FREE_DISC = path_attr(**{
        "PATH": "Status,Resources,disk_free",
        "ATTR": "free_disc"
    })

    STATUS_PORT = "Status,Interfaces,Fixed,Data,status"

    ETR_INPUTS = path_attr(**{
        "PATH": "Etr290ExportData,input",
        "ATTR": (("current_bitrate", "effectiveBitrate"),
                 ("min_signal_level", "minSignalLevel"),
                 ("max_signal_level", "maxSignalLevel"),
                 ("max_centre_frequency_offset", "maxCentreFrequencyOffset"),
                 ("max_current_bitrate", "maximumEffectiveBitrate"), "id",
                 "name", "description", "symbolrate", "minSnr", "minMer",
                 ("symbolrate_offset", "maxSymbolRateOffset")
        )
    })

TEMP_PATH = "/tmp/send2zabbix/"
AUTODISCOVERY_SEND_PERIOD = 12
AUTODISCOVERY_SEND_TIMESTAMP = "timestamp"
TIMEOUT = 900
URL_REQUEST_TIMEOUT = 10
TIME_SERVER = ''
ZABBIX_HOST = ""
ZABBIX_PORT = "10051"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
