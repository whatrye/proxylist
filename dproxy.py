#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import threading
import geoip2.database

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

#下载代理文件
def downloadProxylist():
    print('downloading socks5 proxylist...')
    r1 = requests.get('https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt')
    b = r1.text.split()
    f = open('dproxylist_socks5.txt','w')
    for line in range(0,len(b)):
        f.write(b[line]+'\n')
    f.close()

    geoipReader = geoip2.database.Reader('GeoLite2-City.mmdb')
    '''
    f = open('dproxylist_socks5.json','w')
    str1 = {}
    f.write('[')
    for line in range(0,len(b)-1):
        c = b[line].split(':')
        str1 = '{"type":"socks5",'+'"host":'+'"'+c[0]+'",'+'"port":'+str(c[1])+',"country":'+ '"'+str(geoipReader.city(c[0]).country.iso_code)+'"'
        f.write( str1 +'},\n')
    c = b[len(b)-1].split(':')
    str2 = '{"type":"socks5",'+'"host":'+'"'+c[0]+'",'+'"port":'+str(c[1])+',"country":'+ '"'+str(geoipReader.city(c[0]).country.iso_code)+'"'
    f.write( str2 + '}]')
    f.close()
    '''
    f = open('dproxylist_socks5.json','w')
    outlist = []
    str1 = {}
    for line in range(0,len(b)-1):
        c = b[line].split(':')
        str1['type'] = 'socks5'
        str1['host'] = c[0]
        str1['port'] = c[1]
        str1['country'] = geoipReader.city(c[0]).country.iso_code
        outlist.append(str1)
    json.dump(outlist,f)
    f.close()

    print('downloading http proxylist...')
    r = requests.get('https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list')
    f = open('dproxylist.txt','w')
    f.write(r.text)
    f.close()
    data = r.text.split("\n")
    data = list(filter(None,data))

    #保存为json
    #js = json.dumps(data)

    lendata= len(data)
    f = open('dproxylist.json','w')
    f.write('[')
    for i in range(0,len(data)-1):
        if data[i]:
            f.write(data[i] + ',\n')
    f.write(data[lendata-1])
    #json.dump(data,f,ensure_ascii=False)
    #f.write(js)
    f.write(']')
    f.close()

    '''
    for i in range(0,len(data)-1):
        if data[i]:
            del data[i]['from']
    '''
    #二次处理输出文件
    f = open('dproxylist.json','r')
    data = json.load(f)
    f.close()
    for item in data:
        del item['from']
    f = open('dproxylist.json','w')
    json.dump(data,f,ensure_ascii=False)
    f.close()
    

    return data

#验证
'''
def testIP(proxyQueue):
    while True:
        try:
            proxy = proxyQueue.get_nowait()
            j = proxyQueue.qsize()
        except Exception as e:
            break

        try:
            proxy1 = {"http":proxy['host'] + ':' + str(proxy['port'])}
            r = requests.get(testurl, headers = headers, proxies = proxy1, timeout = 10)
            print(proxy['host'] + ':' + proxy['port'] + ' - ' + str(r.status_code) + "\r\n")

            if r.status_code == 200:
                global proxyOut
                proxyOut.append(proxy)
        except Exception as e:
            print(proxy['host']+':'+str(proxy['port']) + ' - error' + "\r\n")
            #print(proxy['http'] , e , "\r\n")
'''
threadNum = 300
#主程序
def main():
    global proxyOut
    #开始下载代理文件
    data = downloadProxylist()

main()
