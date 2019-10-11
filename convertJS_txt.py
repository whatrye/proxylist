#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import threading
import queue,re,sys

def convertJS_txt(infile):
    fr = open(infile,'r')
    f = open('bbb.txt','w')
    jsdata = json.load(fr)
    for item in jsdata:
        f.write(item['host']+':'+str(item['port'])+'\n')

convertJS_txt(sys.argv[1])
