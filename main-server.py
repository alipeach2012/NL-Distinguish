#!coding:utf8

from http.server import SimpleHTTPRequestHandler,HTTPServer, CGIHTTPRequestHandler
from socketserver import TCPServer
from urllib.parse import urlsplit
import io
import shutil
import json

import math
import pickle as pk
import numpy as np
import os



    
default_info='请点击答案按钮或者直接键盘输入答案（N or L，其他任意键退出）'
info_good=   '              你真棒，恭喜你答对了              '
info_bad=    '              你错了，下次请努力              '

def find_next():
    global i,words,pinyins,n_pinyin,ans,Text,Stat,index
    Stat[:,2]=Stat[:,2]/np.sum(Stat[:,2])
    i=i+1
    while i<n_pinyin and pinyins[i][0]!='n' and pinyins[i][0]!='l':
        i=i+1
    if i==n_pinyin:
        index = np.random.choice(range(n), p = Stat[:,2].ravel())
        words=words_list[index]
        pinyins=pinyins_list[index]
        n_pinyin=len(pinyins)
        i=0
        while i<=n_pinyin and pinyins[i][0]!='n' and pinyins[i][0]!='l':
            i=i+1
        if pinyins[i][0]=='n':
            ans='n'
        if pinyins[i][0]=='l':
            ans='l'

   
def do_check_ans(guess):
    global index,Stat,Text,ans,word,info,info_bad,defualt_info,info_good
    if guess==ans:
        Text="你真棒"
        Stat[index,2]/=2
        Stat[index,1]+=1
    else:
        Text="你错了，这是"+words[i]
        Stat[index,2]*=2
    Stat[index,0]+=1
    find_next()
    Text=Text+','+words+' 中的 '+words[i]+' 是 N 还是 L?'   
    return(Text)

  
def do_exit():
    with open('stat.pk', 'wb') as f:
        pk.dump(Stat,f)
    Text='学习情况已记录，欢迎下次继续！！'   
    return(Text)
    
        
if not os.path.exists('words.pk'):
    
    dict_file=open('large_pinyin.txt',encoding='utf-8')
    
    words_list=[]
    pinyins_list=[]
    while True:
        content = dict_file.readline()
        if not content:
            break
        if  content[0]!='#' :
            temp=content.split(':')
            words=temp[0]
            
            pinyins=temp[1].strip()
            if pinyins[-1]=='\n':
                del(pinyins[-1])
            pinyins=pinyins.split(' ')
            for   pinyin in pinyins:
                if pinyin[0]=='n' or pinyin[0]=='l':
                    words_list.append(words)
                    pinyins_list.append(pinyins)
                    break
    dict_file.close()
    with open('words.pk', 'wb') as f:
        pk.dump(words_list, f)
    with open('pinyins.pk', 'wb') as f:
        pk.dump(pinyins_list, f)



else:

    with open('words.pk', 'rb') as f:
        words_list=pk.load(f)
    with open('pinyins.pk', 'rb') as f:
        pinyins_list=pk.load(f)
 
n=len(words_list)

if os.path.exists('stat.pk'):
    with open('stat.pk', 'rb') as f:
        Stat=pk.load(f)  
else:
    Stat=np.zeros((n,3))
    Stat[:,2]=1
    Stat[:,2]=Stat[:,2]/np.sum(Stat[:,2])
    
index = np.random.choice(range(n), p = Stat[:,2].ravel())
words=words_list[index]
pinyins=pinyins_list[index]
n_pinyin=len(pinyins)
i=0
while i<=n_pinyin and pinyins[i][0]!='n' and pinyins[i][0]!='l':
    i=i+1
if pinyins[i][0]=='n':
    ans='n'
if pinyins[i][0]=='l':
    ans='l'
Text=words+' 中的 '+words[i]+' 是 N or L?'   



enc = "UTF-8"
PORT=1019


RETURN_DATA_temp = '{"returnCode": "0","returnErrorSolution": "","returnMessage": "","returnValue": {"reply": "我是要说的话12344321","resultType": "ASK_INF","actions": [],"properties": {},"executeCode": "SUCCESS","msgInfo": ""}}'

#定义数据处理模块--此部分可放于外部引用文件

class dataHandler():
    #接口分发
    def run(self,path,args):
        
        index = path.replace("/","")
        print ("dataHandler"        ,index)
        switch={
            "BaseInfo": self.getBaseInfo,
            "Monitor": self.getMonitor
            }
        return switch[index](args)
    #接口具体实现
    def getBaseInfo(self,args):
        return "BaseInfo:"+args
    def getMonitor(self,args):
        return "Monitor"+args

#服务环境搭建
class ServerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):  
        print('-----------------------------')
        parsed=urlsplit(self.path)
        mpath=parsed.netloc+parsed.path
        margs=parsed.query
        print("do_GET")
        print(['margs is: ',margs])
        print('------------------------------')
        SimpleHTTPRequestHandler.do_GET(self)
        
    def do_POST(self):
        print('-----------------------------')
        print ("do_POST")
        parsed=urlsplit(self.path)
        mpath=parsed.netloc+parsed.path
        margs=parsed.query
        datas = self.rfile.read(int(self.headers['content-length']))
        print('receive data:')
        print (datas.decode(enc))
        print('-----------------------------')
        self.do_action(json.loads(datas.decode(enc)))
    #请求处理方法
    def do_action(self, data_receive):    
        global Text,ans
        print('-----------------------------')
        print ("do_POST")
        if  data_receive['intentName']=='pystart':
            print('start game')
            Text=words+' 中的 '+words[i]+' 是 N 还是 L?'
            Text='欢迎来到王大神陪你练拼音，游戏就要开始了，下面开始第一题，'+Text
            print ("Output text：")
            print (Text)
            self.outputtxt(RETURN_DATA_temp.replace('我是要说的话12344321',Text))
        if  data_receive["intentName"]=="pyanswer":
            print('得到回答')
            print(['标准答案是：',ans])
            guess=data_receive['slotEntities'][0]['standardValue']
            print(['标准答案是：',guess])
            Text=do_check_ans(guess)
            print ("Output text：")
            print (Text)
            self.outputtxt(RETURN_DATA_temp.replace('我是要说的话12344321',Text))
        if  data_receive['intentName']=='pyend':
            print('结束游戏')
            Text=do_exit()
            print ("Output text：")
            print (Text)
            self.outputtxt(RETURN_DATA_temp.replace('我是要说的话12344321',Text).replace('ASK_INF','RESULT'))
        print('-----------------------------')
            
           
            
            
            
            
    #数据返回到前台
    def outputtxt(self, content):
        print ("outputtxt")
        content=content.encode(enc)
        f = io.BytesIO()
        f.write(  content )
        f.seek(0)
        self.send_response(200)  
        self.send_header("Content-type", "text/html; charset=%s" % enc)  
        self.send_header("Content-Length", str(len(content)))  
        self.end_headers()  
        shutil.copyfileobj(f,self.wfile)
        #SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

#web服务主程序
httpd = TCPServer(("", PORT), ServerHandler)
print ("serving at port", PORT)
httpd.serve_forever()