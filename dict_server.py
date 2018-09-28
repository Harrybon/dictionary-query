# dict_server.py
#!/usr/binenv/ python3
#coding=utf-8

'''
name: wangbo
email: 1414398794@qq.com
date: 2018-9
introduce: dict_search client
env: python3.5
'''
from socket import *
import os
import time
import signal
import sys
import pymysql

#定义全局变量
DICT_TEXT  = 'dict.txt'
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

#循环接受客户端请求,处理请求类型
def do_child(c,db):
    while True:
        data = c.recv(128).decode()
        print(c.getpeername(),':',data)
        if data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == 'L':
            do_login(c,db,data)
        elif data[0] == 'M':
            do_match(c,db,data)
        elif data[0] == 'H':
            do_hist(c,db,data)
        elif (not data) or data[0] == 'E':
            c.close()
            sys.exit(0)

def do_register(c,db,data):
    L = data.split(' ')
    name = L[1]
    passwd = L[2]
    cursor = db.cursor()
    sql = "select * from user where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchone()
    if r != None:
        s.send(b'name repate')
        return
    else:
        sql = "insert into  user (name,passwd)\
         values ('%s','%s')"%(name,passwd)
        try:
            cursor.execute(sql)
            db.commit()
            c.send(b'name is aviliable')
        except:
            db.rollback()
            c.send(b'FALL')
            return
        else:
            print("%s注册成功"%name)

def do_login(c,db,data):
    L = data.split(' ')
    name = L[1]
    passwd = L[2]
    cursor = db.cursor()
    sql = "select * from user where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchone()
    if r!= None:
        sql = "select * from user where passwd='%s'"%passwd
        cursor.execute(sql)
        r = cursor.fetchone()
        if r!= None:
            c.send(b'match success')
            do_match(c,db,data)
        else:
            c.send(b'match failed')
    else:
        c.send(b'FAILED')

def do_match(c,db,data):
    L = data.split(' ')
    word = L[1]
    name = L[2]
    cursor = db.cursor()
    def hist_insert():
        tm = time.ctime()
        sql = "insert into hist \
        (name,word,time) value ('%s','%s','%s')"%(name,word,tm)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    sql = "select * from words where word='%s'"%word
    cursor.execute(sql)
    r = cursor.fetchone()
    if r != None:
        hist_insert()
        c.send(b'OK')
        # time.sleep(0.3)
        interpret = r[2]
        print(interpret)
        c.send(interpret.encode())
    else:
        c.send(b'FAILED')


def do_hist(c,db,data):
    L = data.split(' ')
    name = L[1]
    cursor = db.cursor()
    sql = "select * from hist where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchall()
    if r != None:
        c.send(b'OK')
        n = 0
        for i in r:
            n += 1
            if n > 20:
                break
            else:
                msg = "%s %s %s"%(i[1],i[2],i[3])
                print(msg)
                c.send(msg.encode())
        time.sleep(0.1)
    else:
        c.send(b'FAILED')

def main():
    #创建数据库连接
    db = pymysql.connect\
    ('localhost','root','123456','dict')
    
    #创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    #父进程中忽略子进程状态改变，子进程退出自动由系统处理
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            c,addr = s.accept()
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print('Error:',e)
            continue
        
        #为客户端创建新的子进程
        pid = os.fork()

        #子进程处理具体请求
        if pid == 0:
            s.close()#子进程中s无用
            # print('子进程处理')
            print('处理请求中')
            do_child(c,db)

        #是父进程后者创建失败都继续等待下个客户端连接
        else:
            c.close()#父进程c无用
            continue

if __name__ == '__main__':
    main()