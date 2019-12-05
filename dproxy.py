#!python3
# -*- coding: UTF-8 -*-

import requests
import json
import threading
import geoip2.database

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

#
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

#下载代理文件
def downloadProxylist():
    null = 'unknow'

    #download HTTP from proxyscrape.com
    try:
        print('download from proxyscrape, HTTP')
        r2 = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=1500&country=all&ssl=all&anonymity=all',headers = headers,timeout = 15)
        f = open('proxyscrapeHttp.txt','w')
        f.write(r2.text)
        f.close()
        fr = open('proxyscrapeHttp.txt','r')
        lines = fr.readlines()
        fr.close()
        datas = converttxt_js(lines,'http')
        f = open('proxyscrapeHttp.json','w')
        json.dump(datas,f)
        f.close()
    except Exception as e:
        print('download error',e)

    #download socks5 from proxyscrape.com
    try:
        print('download from proxyscrape, Socks5')
        r3 = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=2000&country=all',headers = headers,timeout = 15)
        f = open('proxyscrapeSocks5.txt','w')
        f.write(r3.text)
        f.close()
        fr = open('proxyscrapeSocks5.txt','r')
        lines = fr.readlines()
        fr.close()
        datas = converttxt_js(lines,'socks5')
        f = open('proxyscrapeSocks5.json','w')
        json.dump(datas,f)
        f.close()
    except Exception as e:
        print('download error',e)

    #download from proxy-list.download
    try:
        print('download from proxy-list, HTTP')
        r4 = requests.get('https://www.proxy-list.download/api/V1/get?type=http&anon=elite',headers = headers,timeout = 15)
        f = open('proxylistHttp.txt','w')
        f.write(r4.text)
        f.close()
        fr = open('proxylistHttp.txt','r')
        lines = fr.readlines()
        fr.close()
        datas = converttxt_js(lines,'http')
        f = open('proxylistHttp.json','w')
        json.dump(datas,f)
        f.close()
    except Exception as e:
        print('download error',e)
        
    #download from proxy-list.download
    try:
        print('download from proxy-list, Socks5')
        r4 = requests.get('https://www.proxy-list.download/api/V1/get?type=socks5&anon=elite',headers = headers,timeout = 15)
        f = open('proxylistSocks5.txt','w')
        f.write(r4.text)
        f.close()
        fr = open('proxylistSocks5.txt','r')
        lines = fr.readlines()
        fr.close()
        datas = converttxt_js(lines,'socks5')
        f = open('proxylistSocks5.json','w')
        json.dump(datas,f)
        f.close()
    except Exception as e:
        print('download error',e)

    #download from github
    try:
        print('downloading http proxylist...')
        r = requests.get('https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list',headers = headers,timeout = 15)
        #https://cdn.jsdelivr.net/gh/fate0/proxylist/proxy.list
        f = open('dproxylist.txt','w')
        f.write(r.text)
        f.close()
        data = r.text.split("\n")
        data = list(filter(None,data))

        #保存为json
        outlist = []
        for item in data:
            a = eval(item)
            del a['from']
            outlist.append(a)
        f = open('dproxylist.json','w')
        json.dump(outlist,f,ensure_ascii=False)
        f.close()
    except Exception as e:
        print('download error',e)

    #download from github
    try:
        print('downloading socks5 proxylist...')
        r1 = requests.get('https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',headers = headers,timeout = 15)
        #https://cdn.jsdelivr.com/gh/hookzof/socks5_list/proxy.txt
        b = r1.text.split()
        f = open('dproxylist_socks5.txt','w')
        for line in range(0,len(b)):
            f.write(b[line]+'\n')
        f.close()

        geoipReader = geoip2.database.Reader('GeoLite2-City.mmdb')
        outlist = []
        for line in range(0,len(b)):
            str1 = {}
            c = b[line].split(':')
            str1['type'] = 'socks5'
            str1['host'] = c[0]
            str1['port'] = c[1]
            try:
                cc = str(geoipReader.city(c[0]).country.iso_code)
                if cc == 'None':
                    cc = 'unknow'
                str1['country'] = cc
            except Exception as e:
                str1['country'] = 'unknow'
            outlist.append(str1)
        f = open('dproxylist_socks5.json','w')
        json.dump(outlist,f)
        f.close()
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
