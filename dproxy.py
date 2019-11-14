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
                str3['country'] = 'unknow'
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
                str3['country'] = 'unknow'
            data.append(str3)
    return data

#下载代理文件
def downloadProxylist():
    null = 'unknow'
    try:
        print('downloading socks5 proxylist...')
        r1 = requests.get('https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',headers = headers,timeout = 15)
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
        outlist = []
        for line in range(0,len(b)):
            str1 = {}
            c = b[line].split(':')
            str1['type'] = 'socks5'
            str1['host'] = c[0]
            str1['port'] = c[1]
            try:
                str1['country'] = geoipReader.city(c[0]).country.iso_code
            except Exception as e:
                str1['country'] = 'unknow'
            #outlist.append(eval(str(str1)))  #why ? eval(str(str1)),if append(str1) outlist all data would be last record .
            outlist.append(str1)
            #print(str1)
        #print(outlist)
        f = open('dproxylist_socks5.json','w')
        json.dump(outlist,f)
        f.close()
    except Exception as e:
        print('download error',e)

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


    try:
        print('downloading http proxylist...')
        r = requests.get('https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list',headers = headers,timeout = 15)
        f = open('dproxylist.txt','w')
        f.write(r.text)
        f.close()
        data = r.text.split("\n")
        data = list(filter(None,data))

        #保存为json
        #js = json.dumps(data)
        '''
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

        outlist = []
        for item in data:
            a = eval(item)
            del a['from']
            outlist.append(a)
        f = open('dproxylist.json','w')
        json.dump(outlist,f,ensure_ascii=False)
        f.close()

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
        '''
    except Exception as e:
        print('download2 error',e)

    return 


threadNum = 300
#主程序
def main():
    global proxyOut
    #开始下载代理文件
    data = downloadProxylist()

if __name__ == '__main__':
    main()
