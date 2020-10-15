#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import lib.utils as utils


def jdumps(o):
    return json.dumps(o, ensure_ascii=False)


def i_m(base_metric, tpl, **kwargs):
    if not kwargs:
        return ".".join([base_metric, tpl])

    prep_kwargs = {
        kw: _str_prep(kwargs[kw]) for kw in kwargs
    }
    return ".".join([base_metric, tpl.format(**prep_kwargs)])


def z_m(tpl, **kwargs):
    prep_kwargs = {
        _str_prep(kw): _str_prep(kwargs[kw]) for kw in kwargs
    }
    return tpl.format(**prep_kwargs)


def _str_prep(s):
    if isinstance(s, (int, float)):
        s = str(s)
    return reduce(
        lambda s, d: s.replace(d[0], d[1]),
        ((".", "_"), ("_[", "."), ("]", "")),
        s
    )

def transliterate(name):
    to_replace = {'ж': 'zh', 'о': 'o', 'п': 'p', 'а': 'a', 'б': 'b', 'в': 'v',
                  'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'з': 'z', 'и': 'i',
                  'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'р': 'r',
                  'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c',
                  'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '',
                  'э': 'e', 'ю': 'u', 'я': 'ja', 'А': 'a', 'Б': 'b', 'В': 'v',
                  'Г': 'g', 'Д': 'd', 'Е': 'e', 'Ё': 'e', 'Ж': 'zh', 'З': 'z',
                  'И': 'i', 'Й': 'i', 'К': 'k', 'Л': 'l', 'М': 'm', 'Н': 'n',
                  'О': 'o', 'П': 'p', 'Р': 'r', 'С': 's', 'Т': 't', 'У': 'u',
                  'Ф': 'Х', 'Ц': 'c', 'Ч': 'cz', 'Ш': 'sh', 'Щ': 'scz', 'Ъ': '',
                  'Ы': 'y', 'Ь': '', 'Э': 'e', 'Ю': 'u', 'Я': 'ja', ',': '',
                  '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '', '$': '',
                  '%': '', '^': '', '&': '', '*': '', '(': '', ')': '',
                  '=': '', '+': '', ':': '', ';': '', '<': '', '>': '', '\'': '',
                  '"': '', '\\': '', '/': '', '№': '', '[': '', ']': '', '{': '',
                  '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i', 'Є': 'e',
                  u'\x01': '', u'\x05': ''}

    for key in to_replace:
        try:
            name = name.replace(unicode(key), to_replace[key])
        except:
            try:
                name = name.replace(key, to_replace[key])
            except:
                pass
    return name


def to_zabbix(analyzer_name, raw_metrics):
    metrics = {
        "autodiscovery": [],
        "static": [],
        "dynamic": []
    }
    m_autodiscovery = metrics["autodiscovery"].append
    m_static = metrics["static"].append
    m_dynamic = metrics["dynamic"].append

    mcasts = set()
    mcast_sids = set()
    mcast_sids_pids = set()
    qam_tss = set()
    qam_tss_sids = set()
    for ts in raw_metrics["tss"]:
        mcasts.add(ts)
        ts_info = raw_metrics["tss"][ts]
        for svc in ts_info["services"]:
            if svc == "count":
                continue
            svc_info = ts_info["services"][svc]
            mcast_sid = z_m("{ts}*SID-{sid}", ts=ts, sid=svc)
            mcast_sids.add(mcast_sid)
            for pid in svc_info["pids"]:
                mcast_sid_pid = z_m("{mcast_sid}*PID-{pid}", mcast_sid=mcast_sid, pid=pid)
                mcast_sids_pids.add(mcast_sid_pid)

    m_autodiscovery((analyzer_name, "get_ts", jdumps({"data": [{"{#TS}": _str_prep(ts)} for ts in mcasts]})))
    if raw_metrics.get("is_scr", False):
        m_autodiscovery((analyzer_name, "get_sid", jdumps({"data": [{"{#SID}": _str_prep(sid)} for sid in mcast_sids]})))

    if raw_metrics.get("is_rgs", False):
        for qts in raw_metrics["qam"]["tss"]:
            qam_tss.add(qts)
            for qsvc in raw_metrics["qam"]["tss"][qts]["services"]:
                qam_tss_sids.add(z_m("{qts}*SID-{qsid}", qts=qts, qsid=qsvc))

        m_autodiscovery((analyzer_name, "get_qam", jdumps({"data": [{"{#QAM}": _str_prep(qam)} for qam in qam_tss]})))

        m_autodiscovery((analyzer_name, "get_qam_sid", jdumps({"data": [{"{#QAM_SID}": _str_prep(qam)} for qam in qam_tss_sids]})))

        for qts in raw_metrics["qam"]["tss"]:
            ts_data = raw_metrics["qam"]["tss"][qts]
            for p_name in (
                ("current_bitrate", "net_bitrate"),
                ("max_centre_frequency_offset", "frequency_offset"),
                ("minSnr", "snr"),
                ("minMer", "mer"),
                "min_signal_level", "max_signal_level", "sid_count"):
                if isinstance(p_name, tuple):
                    p_real_name, p_name = p_name
                    value = utils.get(ts_data, p_real_name)
                else:
                    value = utils.get(ts_data, p_name)
                if isinstance(value, basestring):
                    value = value.split(" ")[0]
                metric = z_m("{p_name}_[{qts}]", p_name=p_name, qts=qts)
                m_dynamic((analyzer_name, metric, value))

            for qsvc in raw_metrics["qam"]["tss"][qts]["services"]:
                qsvc_data = raw_metrics["qam"]["tss"][qts]["services"][qsvc]
                metric = z_m("pids_[{qts}*SID-{qsvc}]", qts=qts, qsvc=qsvc)
                m_dynamic((analyzer_name, metric, qsvc_data["pid_count"]))

    for p_name in ("uptime", "bitrate", "cpu_temp", "free_mem", "free_disc", "port", "version", "time",
                   "time_qam", "time_qam_diff", "time_eth", "time_eth_diff"):

        m_static((analyzer_name, p_name, utils.get(raw_metrics, p_name)))

    tss_data = raw_metrics.get("tss", {})
    for ts in tss_data:
        ts_data = raw_metrics["tss"][ts]
        for p_name in ("net_bitrate", "cc_errors",
                       "crc", ("mlrerr1m", "mlr"), ("iatPeak1m", "iat")):

            if isinstance(p_name, tuple):
                p_real_name, p_name = p_name
                value = utils.get(ts_data, p_real_name)
            else:
                value = utils.get(ts_data, p_name)
            metric = z_m("{p_name}_[{ts}]", p_name=p_name, ts=ts)
            m_dynamic((analyzer_name, metric, value))

        if raw_metrics.get("is_reciv", False):
            value = utils.get(ts_data, "scrambled")
            metric = z_m("scrambled_[{ts}]", ts=ts)
            m_dynamic((analyzer_name, metric, value))

        if raw_metrics.get("is_scr", False):
            value = utils.get(ts_data, "not_existed")
            metric = z_m("no_cktv_tabes_[{ts}]", ts=ts)
            m_dynamic((analyzer_name, metric, value))
            value = utils.get(ts_data, "dst_addr")
            metric = z_m("dst_addr_[{ts}]", ts=ts)
            m_dynamic((analyzer_name, metric, value))

        if raw_metrics.get("is_rgs", False) :
            value = utils.get(ts_data, "dst_addr")
            metric = z_m("dst_addr_[{ts}]", ts=ts)
            m_dynamic((analyzer_name, metric, value))

        services_data = ts_data.get("services", None)
        if not services_data:
            continue
        for svc in services_data:
            if svc == "count":
                continue
            svc_data = ts_data["services"][svc]
            sid = svc_data["id"]
            value = utils.get(svc_data, "bitrate")
            metric = z_m("net_bitrate_[{ts}*SID-{sid}]", ts=ts, sid=sid)
            m_dynamic((analyzer_name, metric, value))

            if raw_metrics.get("is_src", False):
                value = svc_data.get("scrambled_ok", "NO_DATA")
                metric = z_m("scramble_[{ts}*SID-{sid}]", ts=ts, sid=sid)
                m_dynamic((analyzer_name, metric, value))

            if "pids_ok" in svc_data:
                value = utils.get(svc_data, "pids_ok")
                metric = z_m("no_cktv_pid_[{ts}*SID-{sid}]", ts=ts, sid=sid)
                m_dynamic((analyzer_name, metric, value))

            if "scrambled_ok" in svc_data:
                value = utils.get(svc_data, "scrambled_ok")
                metric = z_m("scramble_[{ts}*SID-{sid}]", ts=ts, sid=sid)
                m_dynamic((analyzer_name, metric, value))

    return metrics