#!python3
# -*- coding: UTF-8 -*-

import requests
import json
import threading
import queue,re,sys

def convertJS_txt(infile):
    fr = open(infile,'r')
    jsdata = json.load(fr)
    fr.close()
    f = open('bbb.txt','w')
    for item in jsdata:
        f.write(item['host'] + ':' + str(item['port']) + ' ' + item['country'] + '\n')
    f.close()

if __name__ == '__main__':
    #print(__name__)
    convertJS_txt(sys.argv[1])
