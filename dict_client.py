# dict_client.py
#!/usr/binenv/ python3
#coding=utf-8

'''
name: wangbo
email: 1414398794@qq.com
date: 2018-9
introduce: dict_search server
env: python3.5
'''
from socket import *
import sys
import signal
import getpass

def do_match(s,name):
    tem = input('请输入查询单词内容：')
    msg = "M {} {}".format(tem,name)
    s.send(msg.encode())
    data = s.recv(128).decode()
    print(data)
    if data == 'OK':
        print('ooooo')
        data = s.recv(2048).decode()
        print(tem,':',data)
    else:
        print('没有查询到内容')




def do_hist(s,name):
    name = input('请输入要查询的用户名')
    msg = "H {}".format(name)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        data = s.recv(1024).decode()
        print(data)
    else:
        print('没有查询到信息')

def do_query(s,name):
    while True:
        print('''
            =========Welcome　query=============
            |-- 1.查询　2.历史记录　3.退至主界面--　　|
            ===================================
            ''')
        try:
            cmd = int(input('请输入选项：'))
        except:
            print('输入错误')
            continue
        if cmd == 1:
            do_match(s,name)
        elif cmd == 2:
            do_hist(s,name)
        elif cmd == 3:
            break
        else:
            print("输入如格式有误，请输入：'1','2','3'")
            sys.stdin.flush()#清除标准输入



def do_request(s,cmd):
    if cmd == 1:
        while True:
            name = input('请输入用户名：')
            passwd = getpass.getpass()
            passwd1 = getpass.getpass('密码确认：')
            if (' ' in name) or (' ' in passwd):
                print('用户名，密码不允许有空格')
                continue
            if passwd != passwd1:
                print('两次密码输入不一致')
                continue

            msg = "R {} {}".format(name,passwd)
            s.send(msg.encode())
            data = s.recv(1024).decode()
            if data == 'name repate':
                print('用户名重复')
                return
            elif data == 'name is aviliable':
                print('注册成功')
                try:
                    cmd = int(input('请选择-查询(1)主界面(2):'))
                except:
                    print("输入错误，请输入：'1','2'")
                if cmd == 1:
                    do_query(s,name)
                if cmd == 2:
                    return
            else:
                print('注册失败')


    elif cmd == 2:
            name = input('请输入用户名：')
            passwd = getpass.getpass()
            passwd1 = getpass.getpass('密码确认：')
            msg ="L {} {}".format(name,passwd)
            s.send(msg.encode())
            data = s.recv(1024).decode()
            if data == 'match failed':
                print('用户名或密码错误')
                return
            elif data == 'match success':
                print('恭喜您登录成功')
                try:
                    cmd = int(input('请选择-查询(1)主界面(2):'))
                except:
                    print("输入错误，请输入：'1','2'")
                if cmd == 1:
                    do_query(s,name)
                if cmd == 2:
                    return
            else:
                print('登录失败')
    
    elif cmd == 3:
        s.send(b'E')
        sys.exit('谢谢使用')
    else:
        print("输入如格式有误，请输入：'1','2','3'")
        sys.stdin.flush()#清除标准输入



#创建网络连接
def main():
    if len(sys.argv) < 3:
        print('输入连接地址端口错误')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)
    s = socket()
    try:
        s.connect(ADDR)
    except Exception as e:
        print(e)
        return
    while True:
        print('''
            =========Welcome=========
            |--1.注册2.登录 3.退出--|
            =========================
            ''')
        try:
            cmd = int(input('请输入选项：'))
        except:
            print('输入错误')
            continue
        do_request(s,cmd)

if __name__ == '__main__':
    main()