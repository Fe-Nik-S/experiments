#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from lib import xmltodict
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
SCRAMBLED = u'да'


class ReferenceBase(object):
    def __init__(self, url):
        self.url = url
        self.data = {}
        self.session = requests.session()
        raw_data = self.request(self.url)
        for c in raw_data:
            mcast, sid, pids, crypt = c["SCR_VYHODNAYA_GRUPPA"], c["SID_TRSC"], c["REQUIRED_PIDS"], c["SHIFROVANIE"]
            #print mcast, sid, crypt, crypt.strip() == SCRAMBLED
            if mcast not in self.data:
                self.data[mcast] = {sid: {"pids": pids.split(",") if pids else [],
                                          "crypt": crypt.strip() == SCRAMBLED}}
            else:
                if sid not in self.data[mcast]:
                    self.data[mcast].update({sid: {"pids": pids.split(",") if pids else [],
                                                    "crypt": crypt.strip() == SCRAMBLED}})

    def request(self, url):
        request = self.session.get(url, verify=False)
        data = request.text.encode("utf-8")

        data = data[1:-1]
        result = []    
      
    	for _ in range(data.count('}')):
            index = data.find('}')
            if index == -1:
                break        
            part =  data[:index+1]        
            result += [json.loads(part)]
            data = data[index+2:]
        return result


    def check(self, sencore_tss):
        for ts_name in sencore_tss:
            ts_data = sencore_tss[ts_name]
            try:
                ts_mcast = ts_data["dst_addr"].split(":")[0]
            except Exception as why:
                logging.exception(why)
                continue
            for sid in ts_data["services"]:
                if sid == "count":
                    continue
                reference = self.data.get(
                    ts_mcast, {}
                ).get(
                    str(sid), {}
                )
                if reference:
                    reference_sid_s = set(reference["pids"])
                    sencore_sid_s = set(map(lambda o: str(o), ts_data["services"][sid]["pids"].keys()))
                    diff = list(reference_sid_s.difference(sencore_sid_s))
                    sencore_tss[ts_name]["services"][sid]["pids_ok"] = ",".join(diff) if diff else "OK"
                    crypt_ok = reference["crypt"] == sencore_tss[ts_name]["services"][sid]["scrambled"]
                    if crypt_ok:
                        sencore_tss[ts_name]["services"][sid]["scrambled_ok"] = 0
                    else:
                        sencore_tss[ts_name]["services"][sid]["scrambled_ok"] = 1
                else:
                    sencore_tss[ts_name]["services"][sid]["pids_ok"] = "REFERENCE_DOES_NOT_EXIST"
                    sencore_tss[ts_name]["services"][sid]["scrambled_ok"] = "REFERENCE_DOES_NOT_EXIST"