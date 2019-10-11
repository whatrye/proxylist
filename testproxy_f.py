#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import threading
import queue,re,sys
'''
用telnet来测试代理是否可连
import telnetlib
try:
    telnetlib.Telnet(ip,port,timeout=2)
    print('success',ip,port)
except:
    print(connect failed')
'''
'''
#下载代理文件
def downloadProxylist():
    r = requests.get('https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list')
    data = r.text.split("\n")
    return data
'''
ipText = ''
proxys = []
proxyQueue = queue.Queue()
proxyOut = []
proxy_type = 'http'
testurl = 'http://kali.org/'
threadNum = 200

#验证
def testIP(proxyQueue):
    global proxy_type,testurl,proxyOut

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    while True:
        try:
            proxy = proxyQueue.get_nowait()
            j = proxyQueue.qsize()
        except Exception as e:
            break
        if proxy['type'] == "socks5":
            proxy1 = {"http":"socks5://"+proxy['host']+':'+str(proxy['port'])}
        else:
            proxy1 = {"http":proxy['host']+':'+ str(proxy['port'])}
        try:
            #socks5代理
            #requests.get('http://www.aaa.com/',proxies = {'http':'socks5://xxx.xxx.xxx.xxx:ppp', 'https':'socks5://xxx.xxx.xxx.xxx:ppp'}, timeout = 10)
            r = requests.get(testurl, headers = headers, proxies = proxy1, timeout = 10)
            print(proxy['host'] + ':'+str(proxy['port']) + ' - ' + str(r.status_code) + "\n")

            '''#待测试
            #title = re.search(r'<title>(.*?)</title>',r.text) #查找网页中有没有title字串，或者查找其它特定字串来验证网页是否正确打开
            print(r.text)
            title = re.search(r'亚洲',r.text) #查找网页中有没有title字串，或者查找其它特定字串来验证网页是否正确打开
            print(title.group(1))
            if title: 
                title = title.group(1)
                print('网页正常')
            else:
                print('网页不正常')
            if title == 'www.aisex.com':
                print("okkkkkk")
            #待测试结束
            '''

            if r.status_code == 200:
                proxyOut.append(proxy)                
        except Exception as e:
            print(proxy['host'] +':'+str(proxy['port'])+ ' - error' + "\r\n")
            #print(proxy['http'] , e , "\r\n")

#主程序
def main():
    global proxy_type,proxyOut
    #处理代理文件
    if len(sys.argv)>1:
        proxy_type = sys.argv[1]
    print('proxy type: '+ proxy_type)
    if proxy_type == 'socks5':
        fr = open('dproxylist_socks5.json','r')
    else:
        fr = open('dproxylist.json','r',encoding='utf-8')

    #初始化代理数组
    jdatas = json.load(fr)
    #print(jdatas)
    #line = fr.readline().strip()
    '''
    for line in jdatas:
        #line = eval(line)
        if proxy_type == "socks5":
            proxy_temp = {"http":"socks5://"+line['host']+':'+str(line['port'])}
        else:
            proxy_temp = {"http":line['host']+':'+ str(line['port'])}
        
        if proxy_temp not in proxys: #去除重复的proxy
            proxys.append(proxy_temp)
        line = fr.readline()

    fr.close()
    print(proxys)
    print (len(proxys),'proxies in proxylist')
    print ()
    '''
    jdatas_len = len(jdatas)
    for i in range(0,jdatas_len):
        if jdatas[i]['country']!='CN':
            proxyQueue.put(jdatas[i])
    jqueue = proxyQueue.qsize()
    print(jqueue,'/',jdatas_len,' proxies')
        
    fr.close()
    #开始验证
    threadN = threadNum
    if jqueue < threadNum:
        threadN = jqueue
    print(threadN,' threads')
    
    threads=[]
    for i in range(0,threadN):
        thread=threading.Thread(target=testIP,args=(proxyQueue,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    
    #输出文件json和txt

    #proxyOut.sort()
    proxyOut = list(filter(None,proxyOut))
    proxy_len=len(proxyOut)
    print(proxy_len)
    if proxy_len > 0:
        if proxy_type == 'socks5':
            #f = open('ip_f_socks5.json','w') #改成你要存储的位置
            f1 = open('ip_f_socks5.txt','w')
        else:
            #f = open('ip_f.json','w')
            f1 = open('ip_f.txt','w')
        #f.write('[')
        for i in range(0,proxy_len-1):
            if proxyOut[i]:
                #f.write(str(proxyOut[i]))
                #f.write(',\n')
                f1.write(proxyOut[i]['host']+':'+str(proxyOut[i]['port'])+'\n')
        #f.write(str(proxyOut[proxy_len-1]))
        #f.write(']')
        f1.write(proxyOut[i]['host']+':'+str(proxyOut[i]['port']))
        
        #for i in range(0,len(proxyOut)):
        #    f.write(proxyOut[i])
        #f.write('proxy = [\r\n'+ipText+']')
        #f.close()
        f1.close()
    if proxy_type == 'socks5':
        f = open('ip_f_socks5.json','w') #改成你要存储的位置
    else:
        f = open('ip_f.json','w')
    json.dump(proxyOut,f)
    f.close()
    
    print("final: ",proxy_len," proxies")
    print(proxyOut)

main()
