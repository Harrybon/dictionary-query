# dictionary-query
query words | query history list
电子词典

功能说明 ： 

1. 用户可以登录注册
   登录凭借用户名密码即可 如果输入不正确可以重复输入
   注册 要求用户有填写用户名密码，且用户名不能重复。其他信息随意

2. 用户信息可以长期保存在服务器，保证下次登录可以使    用

3. 能够满足多个用户端程序同时操作的情况

4. 功能分为客户端和服务端，客户端运行后即进入第一界    面
   第一界面 ： 登录   注册   退出
5. 登录成功后进入第二界面
   第二界面 ： 查词   查看历史记录  退出

6. 功能说明
   登录 ： 选择登录功能 输入用户名密码，如果成功进入第二界面，不成功保持在第一界面，提示失败原因
   注册 ： 选择注册功能，填写信息，成功后可以保持第一界面或者使用新注册用户直接完成登录到第二界面，失败提示失败原因
   第一界面退出 ： 直接退出客户端
   查词 ： 可以循环输入单词，显示出单词词义
           输入##表示查词结束回到第二界面。如果查询的词不存在则有相应提示

	   单词本 ： 每一行一个单词
	              单词和解释之间一定有空格
		      单词有序排列
            1. 文本查找  2.数据库查找

   历史记录： 选择查看历史记录即打印出用户的查询记录
              可以打印所有记录也可以打印最近10条。
               name     word     time

   第二界面退出 ： 第二界面退出相当于注销，即退回到                 第一界面

项目分析

模块 :  socket 套接字
        pymysql/pymongo
	os   multiprocessing   threading   select

服务端

客户端

1.确定服务端和客户端分为哪些功能，每个功能要做什么工作

服务端 
main（）  ：  
创建套接字，父子进程，子进程处理客户端请求，父进程接受新的连接

login  接受客户端信息 
       数据库匹配
       返回结果

register  接受用户数据
          判断是否重复
          插入数据库返回注册成功
	  用户存在返回注册失败

query     接受用户单词
          通过数据库或者文件查找单词
          将单词结果返回给用户
	  如果没有查到返回相应信息
	  如果查词成功则插入历史记录

history   接受客户请求
          查询数据库返回历史记录
	  如果用户没有历史记录则返回信息

客户端 ：

main：  创建套接字 ----》 连接 ---》 打印一级界面

login   ：  输入用户名密码
            发送给服务端
	        接受返回结果，如果成功则跳转到二级界面
	        失败打印结果

register ： 输入用户名密码
            发送给服务端
	        接受返回结果

query ：   循环输入单词
           发送单词给服务端
     	   接受结果并打印

history ：  发送请求 ---》 接受结果打印


2.确定建立什么样的数据表，表的结构，将表建立起来
  
  user  ： id  name  passwd
  hist  ： id  name  word   time
  words ： id  word  interpret
 
  create table user (id int auto_increment primary key,name varchar(32) not null,passwd varchar(16) default '000000');

  create table hist (id int auto_increment primary key,name varchar(32) not null,word varchar(64) not null,time varchar(64));
  
  create table words (id int auto_increment primary key,word varchar(64),interpret text); 


3. 如果要使用数据库查词则编程将单词本内容存入数据库

4. 搭建框架，实现通信 （创建套接字，设定结构，创建并发）

5. 实现具体框架优化和具体功能

