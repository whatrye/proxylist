#! python3
# -*- coding: UTF-8 -*-

import requests
import json
import threading
import queue,re,sys


'''
#命令行选项输入方法1
import argparse

##ArgumentParser(prog=None,usage=None, description=None, epilog=None, parents=[], formatter_class=argparser.HelpFormatter, prefix_chars='-', fromfile_prefix_chars=None, argument_default=None, conflict_handler='error', add_help=True)
##其中的参数都有默认值，当运行程序时由于参数不正确或者当调用parser.print_help()方法时，会打印这些描述信息。一般只需要传递参数description。
##add_argument(name or flags... [, action] [, nargs] [, const] [, default] [, type] [, choices] [, required] [, help] [, metavar] [, dest])
##其中的常用参数解释如下：
##name or flags: 命令行参数名或者选项，如-p, --port
##action:
##　　　　store: 默认的action模式，存储值到指定变量
##
##　　　　store_const: 存储值在参数的const部分指定，常用来实现非布尔的命令行flag
##
##　　　　store_true/store_false: 布尔开关。store_true的默认值为False，若命令行有输入该布尔开关则值为True。store_false相反
##
##　　　　append: 存储值到列表，该参数可以重复使用
##
##　　　　append_const: 存储值到列表，存储值在参数的const部分指定
##
##　　　　count: 统计参数简写的输入个数
##
##　　　　version: 输出版本信息，然后退出脚本
##
##nargs: 命令行参数的个数，一般用通配符表示： ？表示只用一个，*表示0到多个，+表示1到多个
##default: 默认值
##type: 参数的类型，默认是string类型，还可以是float、int和布尔等类型
##choices: 输入值的范围
##required: 默认为False，若为True则表示该参数必须输入
##help: 使用的帮助提示信息
##dest: 参数在程序中的对应的变量名称，如：add_argument("-a", dest="code_name")，在脚本中用parser.code_name来访问该命令行选项的值

parser = argparse.ArgumentParser(usage='usage tip',description='help info.') #创建解析对象
parser.add_argument('--address',default='2.3.4.5',help='ip address',dest='host') #向该对象中添加使用到的命令行选项和参数
parser.add_argument('--flag',choices=['full','half','none'],default='half',help='empty?')
parser.add_argument('--port',type=int,required=True,help='the port number.must exist')
parser.add_argument('-l','--log',default=False,action="store_true",help='active log info.')
args = parser.parse_args() #解析命令行
print("--address {0}".format(args.host))
print('--flag {0}'.format(args.flag))
print('--port {0}'.format(args.port))
print('-l {0}'.format(args.log))
'''
'''
#命令行选项输入方法2
import getopt
##    options, args = getopt.getopt(args, shortopts, longopts=[])
##    参数args：一般是sys.argv[1:]。过滤掉sys.argv[0]，它是执行脚本的名字，不算做命令行参数。
##    参数shortopts：短格式分析串。例如："hp:i:"，h后面没有冒号，表示后面不带参数；p和i后面带有冒号，表示后面带参数。
##    参数longopts：长格式分析串列表。例如：["help", "ip=", "port="]，help后面没有等号，表示后面不带参数；ip和port后面带冒号，表示后面带参数。
##    返回值options是以元组为元素的列表，每个元组的形式为：(选项串, 附加参数)，如：('-i', '192.168.0.1')
##    返回值args是个列表，其中的元素是那些不含'-'或'--'的参数。
argv = sys.argv[1:]  #过滤掉sys.argv[0]，脚本名
try:
    options,args = getopt.getopt(argv,"hp:i:",["help","ip=","port="])
except getopt.GetoptError:
    sys.exit()

for option,value in options:
    if option in ("-h","--help"):
        print("help")
    if option in ("-i","--ip"):
        print("ip is: {0}".format(value))
    if option in ("-p',"--port"):
        print("port is {0}".format(value))
print("error args: {0}".format(args))

'''


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
    import argparse
    parser = argparse.ArgumentParser(usage='testproxy -t h -i inputfile -o outputfile',description='test proxy.') #创建解析对象
    parser.add_argument('-t','--type',choices=['h','s5'],default='h',dest='proxy_type',help='proxy type: h-http,s-socks5.')
    parser.add_argument('-i','--inputfile',default='dproxylist.json',dest='inputfile',help='json inputfile name.')
    parser.add_argument('-o','--outputfile',default='ip_f.json',dest='outputfile',help='json outputfile name.')
    parser.add_argument('-u','--url',default='http://kali.org/',dest='testurl',help='test url.')
    args = parser.parse_args() #解析命令行

    testurl = args.testurl
    if args.proxy_type == 'h':
        proxy_type = 'http'
    elif args.proxy_type == 's5':
        proxy_type = 'socks5'
    infilename = args.inputfile
    outfilename = args.outputfile
    print(proxy_type,infilename,testurl)
    fr = open(infilename,'r')
    '''
    #处理代理文件
    if len(sys.argv)>1:
        proxy_type = sys.argv[1]
    print('proxy type: '+ proxy_type)
    if len(sys.argv)>2:
        fname = sys.argv[2]
        fr = open(fname,'r')
    else:
        if proxy_type == 'socks5':
            fr = open('dproxylist_socks5.json','r')
        else:
            fr = open('dproxylist.json','r',encoding='utf-8')
    '''
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
            fo = open('ip_f_socks5.json','w') #改成你要存储的位置
        else:
            fo = open('ip_f.json','w')
        json.dump(proxyOut,fo)
        fo.close()

    print(proxyOut)
    print("final: ",proxy_len," proxies")

main()
