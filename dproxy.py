#!python3
# -*- coding: UTF-8 -*-

import requests
import json
import threading
import geoip2.database

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

#下载代理文件
def downloadProxylist():
    try:
        print('downloading socks5 proxylist...')
        r1 = requests.get('https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt')
        b = r1.text.split()
        f = open('dproxylist_socks5.txt','w')
        for line in range(0,len(b)-1):
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
        str1 = {}
        for line in range(0,len(b)-1):
            c = b[line].split(':')
            str1['type'] = 'socks5'
            str1['host'] = c[0]
            str1['port'] = c[1]
            try:
                str1['country'] = geoipReader.city(c[0]).country.iso_code
            except Exception as e:
                str1['country'] = 'null'
            outlist.append(eval(str(str1)))  #why ? eval(str(str1)),if append(str1) outlist all data would be last record .
            #print(str1)
        #print(outlist)
        f = open('dproxylist_socks5.json','w')
        json.dump(outlist,f)
        f.close()
    except:
        print('download error')

    #download HTTP from proxyscrape.com
    r2 = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=1500&country=all&ssl=all&anonymity=all')
    f = open('proxyscrapeHttp.txt','w')
    f.write(r2.text)
    f.close()

    #download socks5 from proxyscrape.com
    r3 = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=2000&country=all')
    f = open('proxyscrapeSocks5.txt','w')
    f.write(r3.text)
    f.close()

    #download from proxy-list.download
    r4 = requests.get('https://www.proxy-list.download/api/V1/get?type=http&anon=elite')
    f = open('proxylistHttp.txt','w')
    f.write(r4.text)
    f.close()


    try:
        print('downloading http proxylist...')
        r = requests.get('https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list')
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
        null = 'null'
        for item in data:
            a = eval(item)
            #if a['country'] == null:
            #    a['country'] = geoipReader.city(a['host']).country.iso_code
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
    except:
        print('download2 error')

    return 

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
