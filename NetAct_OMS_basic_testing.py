#-*- encoding=UTF-8 -*-
'''
Version 0.0.1: main framework
Version 0.0.2: main functions
Version 0.0.3: add settings
Version 0.1.0: first addition for use
Version 0.2.0: opyimize saving files
Version 0.3.0: add events

'''

__author__ = 'zhuo.lv@nokia.com'
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import * 
from subprocess import Popen, PIPE
import os


#Var
root = Tk()
PYBOT_IF_COMMAND=0
FILE_LOCATE=0
OMS_CORR=0
CM=0
FM=0
PM=0
OMS_Sta=0
LOG_PATH=0
CASE_TAG=''

#Function setting
def start_to_run():
    global FILE_LOCATE
    global LOG_PATH
    try:
        openconfig=open('config.txt',"r")
        openlog=open('log_path.txt','r')
        FILE_LOCATE=openconfig.read()
        LOG_PATH=openlog.read()
        openconfig.close()
        openlog.close()
    except Exception as e:
        print(e)

    if(FILE_LOCATE==0) :
        warning = "Configuration file is not loaded.\nPlease load configuration plan first."
        showinfo(title='Warning: no configuration file', message = warning)        
    elif(LOG_PATH==0) :
        warning = "Please specify your location to save logs."
        showinfo(title='Warning: no log path', message = warning)
    elif(PYBOT_IF_COMMAND==0) :
    	warning = "Case is not selected.\nPlease select your test case first."
    	showinfo(title='Warning: no case selected', message = warning)
    else:
        msg = 'Testing will be started with\nConfiguration file: '+FILE_LOCATE+'\nLogs saved to: '+LOG_PATH+'\nConfirm to continue.'
        showinfo(title='Confirm to continue', message = msg)
        multi_tag=0
        global CASE_TAG
        if OMS_CORR % 2 ==1:
            CASE_TAG='oms_corr'
            multi_tag += 1
        if CM % 2 ==1:
            if multi_tag:
                CASE_TAG=CASE_TAG+'AND'
            CASE_TAG=CASE_TAG+'cm'
            multi_tag += 1
        if FM % 2 ==1:
            if multi_tag:
                CASE_TAG=CASE_TAG+'AND'
            CASE_TAG=CASE_TAG+'fm'
            multi_tag += 1
        if PM % 2 ==1:
            if multi_tag:
                CASE_TAG=CASE_TAG+'AND'
            CASE_TAG=CASE_TAG+'pm'
            multi_tag += 1
        if OMS_Sta % 2 ==1:
            if multi_tag:
                CASE_TAG=CASE_TAG+'AND'
            CASE_TAG=CASE_TAG+'oms_sta'
            multi_tag += 1
           
        homedir = os.getcwd()
        PYBOT_COMMAND = r'pybot.bat -V '+FILE_LOCATE+' -d '+LOG_PATH+' -i '+CASE_TAG+' '+homedir+r'\test.html'
        print(PYBOT_COMMAND)

        run_bts=Popen(args=PYBOT_COMMAND,shell=True,stdout=PIPE)
        showinfo(title='Running', message = 'In progress, please wait...\nClick to close.\nReport will be showed once case is done.')
        run_bts.wait()
        pr=run_bts.stdout.readlines()
        showinfo(title='Report', message = pr)

def about():
        string = "Version 0.0.3\nAny concern please contact zhuo.lv@nokia.com"
        showinfo(title='Readme', message = string) 

def set_log_path():
    global LOG_PATH
    LOG_PATH = askdirectory(parent=root,initialdir="/",title='Please pcik a directory')
    string = 'Execution logs will be saved in\n'+LOG_PATH
    showinfo(title='Set log path successfully', message = string)
    try:
        savefile=open('log_path.txt','w')
        savefile.write(LOG_PATH)
        savefile.close()
    except Exception as e:
        print(e)

def load_config_file(): 
    global FILE_LOCATE
    FILE_LOCATE = askopenfilename(title='Open a configuration file', filetypes=[('Python', '*.py *.pyw'), ('All Files', '*')])
    string = 'Configuration file\n' + FILE_LOCATE + '\nhas been loaded'
    showinfo(title='Load file successfully', message = string)
    try:
        savefile=open('config.txt','w')
        savefile.write(FILE_LOCATE)
        savefile.close()
    except Exception as e:
        print(e)

def select_OMS_Corr():
    global PYBOT_IF_COMMAND
    global OMS_CORR
    if OMS_CORR % 2 == 0:
        OMS_CORR += 1
        PYBOT_IF_COMMAND += 1
    else:
        OMS_CORR += 1
        PYBOT_IF_COMMAND -= 1
def select_CM():
    global PYBOT_IF_COMMAND
    global CM
    if CM % 2 == 0:
        CM += 1
        PYBOT_IF_COMMAND += 1
    else:
        CM += 1
        PYBOT_IF_COMMAND -= 1
def select_FM():
    global PYBOT_IF_COMMAND
    global FM
    if FM % 2 == 0:
        FM += 1
        PYBOT_IF_COMMAND += 1
    else:
        FM += 1
        PYBOT_IF_COMMAND -= 1
def select_PM():
    global PYBOT_IF_COMMAND
    global PM
    if PM % 2 == 0:
        PM += 1
        PYBOT_IF_COMMAND += 1
    else:
        PM += 1
        PYBOT_IF_COMMAND -= 1
def select_OMS_Sta():
    global PYBOT_IF_COMMAND
    global OMS_Sta
    if OMS_Sta % 2 == 0:
        OMS_Sta += 1
        PYBOT_IF_COMMAND += 1
    else:
        OMS_Sta += 1
        PYBOT_IF_COMMAND -= 1

#外观设置
menubar = Menu(root)
root.title("NetAct OMS basic testing toolkit")
desc1 = Label(root, text="Please select test case then click run:\n").grid(row = 0, sticky= W)
case1 = Checkbutton(root, text="Corr update", command=select_OMS_Corr).grid(row = 1, sticky= W)
case2 = Checkbutton(root, text="CM verification", command=select_CM).grid(row = 2, sticky= W)
case3 = Checkbutton(root, text="FM verification", command=select_FM).grid(row = 3, sticky= W)
case4 = Checkbutton(root, text="PM verification", command=select_PM).grid(row = 4, sticky= W)
case5 = Checkbutton(root, text="OMS status verification", command=select_OMS_Sta).grid(row = 5, sticky= W)

Button(root, text="Start", command=start_to_run).grid(row = 7, sticky= W)

#创建下拉菜单Run，然后将其加入到顶级的菜单栏中
runmenu = Menu(menubar,tearoff=0)

runmenu.add_command(label="Start", command=start_to_run)
runmenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Run", menu=runmenu)

setmenu = Menu(menubar,tearoff=0)

setmenu.add_command(label="Load configuration file", command=load_config_file)
setmenu.add_command(label="Set log path", command=set_log_path)
menubar.add_cascade(label="Settings", menu=setmenu)

'''#创建另一个下拉菜单eNB
enbmenu = Menu(menubar, tearoff=0)
enbmenu.add_command(label="Settings", command=hello)
enbmenu.add_separator()
enbmenu.add_command(label="Test", command=hello)
menubar.add_cascade(label="eNB",menu=enbmenu)

#创建另一个下拉菜单OMS
omsmenu = Menu(menubar, tearoff=0)
omsmenu.add_command(label="Add", command=hello)
omsmenu.add_command(label="Delete", command=hello)
omsmenu.add_separator()
omsmenu.add_command(label="Test", command=hello)
menubar.add_cascade(label="OMS",menu=omsmenu)

#创建另一个下拉菜单NetAct
namenu = Menu(menubar, tearoff=0)
namenu.add_command(label="Add", command=hello)
namenu.add_command(label="Delete", command=hello)
namenu.add_separator()
namenu.add_command(label="Test", command=hello)
menubar.add_cascade(label="NetAct",menu=namenu)'''

#创建下拉菜单Help
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

#显示菜单
root.config(menu=menubar)

mainloop()
