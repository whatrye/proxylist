#!python3
# -*- coding: UTF-8 -*-

import json
import sys
import geoip2.database

def converttxt_js(lines,proxyType):
    geoipReader = geoip2.database.Reader('GeoLite2-City.mmdb')
    data = []

    if proxyType == 'socks5':
        for item in lines:
            c = item.strip().split(':')
            if len(c[0]) < 5:
                continue
            str3 = {}
            str3['type'] = 'socks5'
            str3['host'] = c[0]
            str3['port'] = c[1]
            try:
                str3['country'] = geoipReader.city(c[0]).country.iso_code
            except Exception as e:
                str3['country'] = 'null'
            data.append(str3)
    else:
        for item in lines:
            c = item.strip().split(':')
            if len(c[0]) < 5:
                continue
            str3 = {}
            str3['type'] = 'http'
            str3['host'] = c[0]
            str3['port'] = c[1]
            try:
                str3['country'] = geoipReader.city(c[0]).country.iso_code
            except Exception as e:
                str3['country'] = 'null'
            data.append(str3)
    return data

if __name__ == '__main__':
    #print(__name__)
    line = []
    fr = open(sys.argv[1],'r')
    lines = fr.readlines()
    fr.close()
    datas = converttxt_js(lines,'http')
    f = open('bbb.json','w')
    json.dump(datas,f)
    f.close()
    print('total %s converted'%len(datas))
