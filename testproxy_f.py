#!python3
# -*- coding: UTF-8 -*-

import requests
import json
import threading
import queue,re,sys,time
#import operator


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

ipText = ''
proxys = []
proxyQueue = queue.Queue()
proxyOutHttp = []
proxyOutSocks = []
proxy_type = 'http'
testurl = 'https://kali.org/'
threadNum = 200

#验证
def testIP(proxyQueue):
    global proxy_type,testurl,proxyOutHttp,proxyOutSocks

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    while True:
        try:
            proxy = proxyQueue.get_nowait()
            j = proxyQueue.qsize()
        except Exception as e:
            break
        if proxy['type'] == "socks5":
            proxy1 = {"http":"socks5://"+proxy['host']+':'+str(proxy['port']),"https":"socks5://"+proxy['host']+':'+str(proxy['port'])}
        else:
            proxy1 = {"http":proxy['host']+':'+ str(proxy['port']),"https":proxy['host']+':'+ str(proxy['port'])}
        try:
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
                if proxy['type'] == "socks5":
                    proxyOutSocks.append(proxy)
                else:
                    proxyOutHttp.append(proxy)
        except Exception as e:
            print(proxy['host'] +':'+str(proxy['port'])+ ' - error' + "\r\n")
            #print(proxy['http'] , e , "\r\n")

#主程序
def main():
    global proxy_type,proxyOutHttp,proxyOutSocks
    import argparse
    parser = argparse.ArgumentParser(usage='testproxy -t h -i inputfile -o outputfile',description='test proxy.') #创建解析对象
    parser.add_argument('-t','--type',choices=['h','s5'],default='h',dest='proxy_type',help='proxy type: h-http,s-socks5.')
    parser.add_argument('-i','--inputfile',default='dproxylist.json',dest='inputfile',help='json inputfile name.')
    parser.add_argument('-o','--outputfile',default='ip_f.json',dest='outputfile',help='json outputfile name.')
    parser.add_argument('-u','--url',default='https://kali.org/',dest='testurl',help='test url.')
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

    #初始化代理数组
    jdatas = json.load(fr)
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
    proxyOutHttp = list(filter(None,proxyOutHttp))
    proxyOutSocks = list(filter(None,proxyOutSocks))
    xproxyOutHttp = sorted(proxyOutHttp, key = lambda proxyOutHttp : proxyOutHttp['host'])
    xproxyOutSocks = sorted(proxyOutSocks, key = lambda proxyOutSocks : proxyOutSocks['host'])
 
    proxyH_len = len(xproxyOutHttp)
    proxyS_len = len(xproxyOutSocks)
    print(proxyH_len)
    #输出Http代理
    if proxyH_len > 0:
        ofname = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        fo = open('ip_Http'+ofname+'.json','w')
        json.dump(xproxyOutHttp,fo)
        fo.close()
        f1 = open('ip_http'+ofname+'.txt','w')
        for i in range(0,proxyH_len):
            if xproxyOutHttp[i]:
                f1.write(xproxyOutHttp[i]['host']+':'+str(xproxyOutHttp[i]['port'])+' '+xproxyOutHttp[i]['country']+'\n')
        #f1.write(proxyOutHttp[i+1]['host']+':'+str(proxyOutHttp[i+1]['port']))
        f1.close()

    #输出Socks5代理
    if proxyS_len > 0:
        ofname = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        fo = open('ip_socks5'+ofname+'.json','w')
        json.dump(xproxyOutSocks,fo)
        fo.close()
        #xproxyOutSocks = sorted(proxyOutSocks, key = operator.itemgetter('host'))
        f1 = open('ip_socks5'+ofname+'.txt','w')
        for i in range(0,proxyS_len):
            if xproxyOutSocks[i]:
                f1.write(xproxyOutSocks[i]['host']+':'+str(xproxyOutSocks[i]['port'])+' '+xproxyOutSocks[i]['country']+'\n')
        #f1.write(proxyOutSocks[i+1]['host']+':'+str(proxyOutSocks[i+1]['port']))
        f1.close()

    print(xproxyOutHttp)
    print("final:")
    print(" Http proxy: ",proxyH_len)
    print(" Socks5 proxy: ",proxyS_len)
    print("OVER!")

if __name__ == '__main__':
    main()
