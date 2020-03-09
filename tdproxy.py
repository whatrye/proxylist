#!python3
# -*- coding: UTF-8 -*-

import requests
import json
import threading
import geoip2.database
import time

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
#proxiess = {"http":"https://127.0.0.1:4477","https":"https://127.0.0.1:4477"}
proxiess = {}

#去除重复
def removeDuplicate(data):
    data2 = []
    data1 = []
    for item in data:
        if item not in data2:
            data2.append(item)
    data1 = sorted(data2)
    return data

#将txt转换为json
def converttxt_js(lines,proxyType):
    geoipReader = geoip2.database.Reader('GeoLite2-City.mmdb')
    data = []
    null = 'unknow'

    for item in lines:
        c = item.strip().split(':')
        if len(c[0]) < 5:
            continue
        str3 = {}
        str3['type'] = 'http'
        if proxyType == 'socks5':
            str3['type'] = 'socks5'
        str3['host'] = c[0]
        str3['port'] = c[1]
        try:
            cy = str(geoipReader.city(c[0]).country.iso_code)
            if cy == 'None':
                cy = 'unknow'
            str3['country'] = cy
        except Exception as e:
            str3['country'] = 'unknow'
        data.append(str3)
    return data

#将json转换为txt
def convertJS_txt(infile):
    fr = open(infile,'r')
    jsdata = json.load(fr)
    fr.close()
    f = open('bbb.txt','w')
    for item in jsdata:
        f.write(item['host'] + ':' + str(item['port']) + ' ' + item['country'] + '\n')
    f.close()

#保存为txt文件
def save2txt(proxyType,data):
    if proxyType == 'socks5':
        f = open('socks5proxy'+ time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.txt','a')
    elif proxyType == 'https':
        f = open('httpsproxy'+ time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.txt','a')
    else:
        f = open('httpproxy'+ time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.txt','a')
    for line in range(0,len(data)):
        f.write(data[line])
    #f.write(data)
    f.close()
    
    
#下载代理文件
def downloadProxylist():
    null = 'unknow'

    #download HTTP from proxyscrape.com
    try:
        print('download from proxyscrape, HTTP')
        r2 = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=1500&country=all&ssl=all&anonymity=all',
                          headers = headers,
                          proxies = proxiess,
                          timeout = 15)
        data2 = r2.text.split("\n")
        data2 = list(filter(None,data2))
        save2txt('http',data2)
##        f = open('proxyscrapeHttp.txt','a')
##        f.write(r2.text)
##        f.close()
##        fr = open('proxyscrapeHttp.txt','r')
##        lines = fr.readlines()
##        fr.close()
##        datas = converttxt_js(lines,'http')
##        f = open('proxyscrapeHttp.json','w')
##        json.dump(datas,f)
##        f.close()
    except Exception as e:
        print('download error',e)

    #download socks5 from proxyscrape.com
    try:
        print('download from proxyscrape, Socks5')
        r3 = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=2000&country=all',
                          headers = headers,
                          proxies = proxiess,
                          timeout = 15)
        data3 = r3.text.split("\n")
        data3 = list(filter(None,data3))
        save2txt('socks5',data3)
##        f = open('proxyscrapeSocks5.txt','w')
##        f.write(r3.text)
##        f.close()
##        fr = open('proxyscrapeSocks5.txt','r')
##        lines = fr.readlines()
##        fr.close()
##        datas = converttxt_js(lines,'socks5')
##        f = open('proxyscrapeSocks5.json','w')
##        json.dump(datas,f)
##        f.close()
    except Exception as e:
        print('download error',e)

    #download http from proxy-list.download
    try:
        print('download from proxy-list, HTTP')
        r4 = requests.get('https://www.proxy-list.download/api/V1/get?type=http&anon=elite',
                          headers = headers,
                          proxies = proxiess,
                          timeout = 15)
        data4 = r4.text.split("\n")
        data4 = list(filter(None,data4))
        save2txt('http',data4)
##        f = open('proxylistHttp.txt','w')
##        f.write(r4.text)
##        f.close()
##        fr = open('proxylistHttp.txt','r')
##        lines = fr.readlines()
##        fr.close()
##        datas = converttxt_js(lines,'http')
##        f = open('proxylistHttp.json','w')
##        json.dump(datas,f)
##        f.close()
    except Exception as e:
        print('download error',e)
        
    #download socks5 from proxy-list.download
    try:
        print('download from proxy-list, Socks5')
        r5 = requests.get('https://www.proxy-list.download/api/V1/get?type=socks5&anon=elite',
                          headers = headers,
                          proxies = proxiess,
                          timeout = 15)
        data5 = r5.text.split("\n")
        data5 = list(filter(None,data5))
        save2txt('socks5',data5)
##        f = open('proxylistSocks5.txt','w')
##        f.write(r4.text)
##        f.close()
##        fr = open('proxylistSocks5.txt','r')
##        lines = fr.readlines()
##        fr.close()
##        datas = converttxt_js(lines,'socks5')
##        f = open('proxylistSocks5.json','w')
##        json.dump(datas,f)
##        f.close()
    except Exception as e:
        print('download error',e)

    #download http from github
    try:
        print('downloading http proxylist from github...')
        r = requests.get('https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list',
                         headers = headers,
                         proxies = proxiess,
                         timeout = 15)
##        https://cdn.jsdelivr.net/gh/fate0/proxylist/proxy.list
##        f = open('dproxylist.txt','w')
##        f.write(r.text)
##        f.close()
        data = r.text.split("\n")
        data = list(filter(None,data))

        #保存为json
        outlisthttp = []
        outlisthttps = []
        for item in data:
            a = eval(item)
            #del a['from']
            if a['type'] == 'https':
                outlisthttps.append(a['host']+':'+str(a['port'])+'\n')
            elif a['type'] == 'http':
                outlisthttp.append(a['host']+':'+str(a['port'])+'\n')
            #outlist.append(a['host']+':'+a['port'])
        save2txt('http',outlisthttp)
        save2txt('https',outlisthttps)
##        f = open('dproxylist.json','w')
##        json.dump(outlist,f,ensure_ascii=False)
##        f.close()
    except Exception as e:
        print('download error',e)

    #download socks5 from github
    try:
        print('downloading socks5 proxylist from github...')
        r1 = requests.get('https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
                          headers = headers,
                          proxies = proxiess,
                          timeout = 15)
        #https://cdn.jsdelivr.com/gh/hookzof/socks5_list/proxy.txt
        data1 = r1.text.split('\n')
        data1 = list(filter(None,data1))
        save2txt('socks5',data1)
##        f = open('dproxylist_socks5.txt','w')
##        for line in range(0,len(b)):
##            f.write(b[line]+'\n')
##        f.close()
##
##        geoipReader = geoip2.database.Reader('GeoLite2-City.mmdb')
##        outlist = []
##        for line in range(0,len(b)):
##            str1 = {}
##            c = b[line].split(':')
##            str1['type'] = 'socks5'
##            str1['host'] = c[0]
##            str1['port'] = c[1]
##            try:
##                cc = str(geoipReader.city(c[0]).country.iso_code)
##                if cc == 'None':
##                    cc = 'unknow'
##                str1['country'] = cc
##            except Exception as e:
##                str1['country'] = 'unknow'
##            outlist.append(str1)
##        f = open('dproxylist_socks5.json','w')
##        json.dump(outlist,f)
##        f.close()
    except Exception as e:
        print('download error',e)

    return 


threadNum = 300
#主程序
def main():
    global proxyOut
    #开始下载代理文件
    data = downloadProxylist()

if __name__ == '__main__':
    main()
