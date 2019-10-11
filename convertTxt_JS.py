#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import sys
import geoip2.database

def converttxt_js(infile):
    geoipReader = geoip2.database.Reader('GeoLite2-City.mmdb')
    fr = open(infile,'r')
    f = open('bbb.json','w')
    data = []
    line = []
    line = fr.readlines()
    #f.write('[')
    for item in line:
        c = item.strip().split(':')
        #str1 = '{"type":"http",'+'"host":'+'"'+c[0]+'",'+'"port":'+c[1]+',"country":'+ '"'+str(geoipReader.city(c[0]).country.iso_code)+'"'
        str3 = {"type":"http","host":c[0],"port":c[1],"country":str(geoipReader.city(c[0]).country.iso_code)}
        data.append(str3)
        #f.write(str1+'},\n')
        #line = fr.readline()
    #str2 = '{"type":"http",'+'"host":'+'"'+c[0]+'",'+'"port":'+c[1]+',"country":'+ '"'+str(geoipReader.city(c[0]).country.iso_code)+'"'
    #f.write( str2 + '}]')
    json.dump(data,f)
    f.close()
    fr.close()

converttxt_js(sys.argv[1])
