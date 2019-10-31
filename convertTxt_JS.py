#! python3
# -*- coding: UTF-8 -*-

import json
import sys
import geoip2.database

def converttxt_js(infile):
    geoipReader = geoip2.database.Reader('GeoLite2-City.mmdb')
    data = []
    line = []
    fr = open(infile,'r')
    line = fr.readlines()
    fr.close()
    #f.write('[')
    for item in line:
        c = item.strip().split(':')
        if len(c[0]) < 5:
            continue
        str3 = {} #str3 need be here
        #str1 = '{"type":"http",'+'"host":'+'"'+c[0]+'",'+'"port":'+c[1]+',"country":'+ '"'+str(geoipReader.city(c[0]).country.iso_code)+'"'
        #str3 = {"type":"http","host":c[0],"port":c[1],"country":str(geoipReader.city(c[0]).country.iso_code)}
        str3['type'] = 'http'
        str3['host'] = c[0]
        str3['port'] = c[1]
        str3['country'] = geoipReader.city(c[0]).country.iso_code

        data.append(str3)
        #f.write(str1+'},\n')
        #line = fr.readline()
    #str2 = '{"type":"http",'+'"host":'+'"'+c[0]+'",'+'"port":'+c[1]+',"country":'+ '"'+str(geoipReader.city(c[0]).country.iso_code)+'"'
    #f.write( str2 + '}]')
    f = open('bbb.json','w')
    json.dump(data,f)
    f.close()

converttxt_js(sys.argv[1])
