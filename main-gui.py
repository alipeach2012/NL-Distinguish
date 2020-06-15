#!coding:utf8

import PIL.Image
from PIL import ImageTk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import math
import matplotlib.pyplot as plt


import pickle as pk
import numpy as np
import time
import pyttsx3
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
    Text=words+' 中的 '+words[i]+' 是 N or L?' 
        
            
def do_check_ans_N():
    global index,Stat,Text,ans,word,info,info_bad,defualt_info,info_good
    if 'n'==ans:
        info.config(text=info_good)
        info.update()
        engine.say("你真棒")
        engine.runAndWait()
        Stat[index,2]/=2
        Stat[index,1]+=1
    else:
        info.config(text=info_bad)
        info.update()
        engine.say("你错了，这是"+words[i])
        engine.runAndWait()
        Stat[index,2]*=2
    Stat[index,0]+=1
    find_next()
    time.sleep(0.2)
    info.config(text=default_info)
    word.config(text=Text)
           
    
def do_check_ans_L():
    global index,Stat,Text,ans,word,info,info_bad,defualt_info,info_good
    if 'l'==ans:
        info.config(text=info_good)
        info.update()
        engine.say("你真棒")
        engine.runAndWait()
        Stat[index,2]/=2
        Stat[index,1]+=1
    else:
        info.config(text=info_bad)
        info.update()
        engine.say("你错了，这是"+words[i])
        engine.runAndWait()
        Stat[index,2]*=2
    Stat[index,0]+=1
    find_next()
    time.sleep(0.2)
    
    info.config(text=default_info)
    word.config(text=Text)
    
def check_ans_input(event):
    if event.char=='n':
        do_check_ans_N()
    elif event.char=='l':
        do_check_ans_L()
    else:
        do_exit()
            
    
    
def do_exit():
    quit_ask = askokcancel('提示','真的要结束么？')
    if quit_ask== True:
        with open('stat.pk', 'wb') as f:
            pk.dump(Stat,f)
        window.destroy()
    
        
if os.path.exists('words.pk'):
    
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

engine = pyttsx3.init()
engine.setProperty('rate', 250)  
engine.say("开始喽，要来咯")
engine.runAndWait()
window = Tk()
window.configure(bg='pink') 
#window.geometry('500x200') 
window.title("NL训练程序")

word = Label(window,text=Text,font=(60),bg='seashell')   #创建标签
word.grid(row=0,column=0,rowspan=2,columnspan=2,padx=5, pady=20)


check_ans_N = Button(window, text="N", width=10, height=2, command=do_check_ans_N)
check_ans_L = Button(window, text="L", width=10, height=2, command=do_check_ans_L)
check_ans_exit = Button(window, text="退出", width=10, height=2, command=do_exit)

check_ans_N.grid(row=2,column=0,ipadx=20, pady=20)
check_ans_L.grid(row=2,column=1,ipadx=20, pady=20)

info = Label(window,text=default_info,width=60,font=(10),bg='seashell')   #创建标签
info.grid(row=3,column=0,rowspan=2,columnspan=2,padx=5, pady=20)
check_ans_exit.grid(row=5,column=0,columnspan=2,padx=5, pady=20)
window.bind("<Key>", check_ans_input)

window.mainloop()


                    
            