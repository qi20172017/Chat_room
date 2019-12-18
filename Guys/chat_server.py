"""
chat room  AID 1910
env: python3.6
author: Levi
socket udp  & fork
"""
from socket import *
import os
import sys
from threading import Event

e1 = Event()
# 服务地址
ADDR = ('0.0.0.0', 8888)

# 存储用户  {name:address}
user = {}

list01 = ['qtx', '小泽玛利亚', '草', '艹', 'cao']
warning_dir = {}
blacklist = []


# 进入处理
def do_login(s, name, addr):
    if name in user or '管理' in name or name in blacklist:
        s.sendto(b'FAIL', addr)
        return
    s.sendto(b'OK', addr)

    # 通知其他人
    msg = "\n欢迎%s进入聊天室" % name
    for i in user:
        s.sendto(msg.encode(), user[i])
    # 将其添加到用户字典
    user[name] = addr


# 聊天
def do_chat(s, name, text):
    msg = "\n%s : %s" % (name, text)
    # admin_eye(s,name,text)
    if cherk(text):
        if name in warning_dir:
            warning_dir[name] += 1
        else:
            warning_dir[name] = 1
        if warning_dir[name] > 4:
            blacklist.append(name)
        if name in blacklist:
            do_quit(s, name)
        text = name + ',发布敏感词汇，警告第%s次！！！' % warning_dir[name]
        name = '管理员'
        msg = "\n%s : %s" % (name, text)

    for i in user:
        # 刨除本人
        if i != name:
            s.sendto(msg.encode(), user[i])


def send_mes(tack,text,name):
    tack.sendto(text.encode(),user[name])

def admin_eye(s,name,text):
    if cherk(text):
        text=name
        send_mes(s,text.encode(),'管理员')
        e1.wait()



def cherk(text):
    for item in list01:
        if item in text:
            return True


# 退出
def do_quit(s, name):
    msg = "\n%s退出群聊" % name
    for i in user:
        if i != name:
            # 告知其他人
            s.sendto(msg.encode(), user[i])
        else:
            # 让他本人的接收进程退出
            s.sendto(b'EXIT', user[i])
    del user[name]


# 功能分发函数
def do_request(s):
    while True:
        # 循环接受请求
        data, addr = s.recvfrom(1024)
        tmp = data.decode().split(' ', 2)
        # 根据请求类型，选择功能模块去处理
        # L   C   Q
        if tmp[0] == 'L':
            do_login(s, tmp[1], addr)  # 具体函数处理具体功能
        elif tmp[0] == 'C':
            do_chat(s, tmp[1], tmp[2])
        elif tmp[0] == 'Q':
            do_quit(s, tmp[1])


def handle_violator(s,name):
    if name in warning_dir:
        warning_dir[name] += 1
    else:
        warning_dir[name] = 1
    do_quit(s,name)
    if warning_dir[name] > 4:
        blacklist.append(name)
    if name in blacklist:
        do_quit(user[name], name)


# 启动函数
def main():
    # udp网络服务
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)

    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        # 管理员消息的发送
        while True:
            text = input("管理员消息:")
            msg = "C 管理员 " + text
            # 将消息从子进程发送给父进程
            s.sendto(msg.encode(), ADDR)
    else:
        do_request(s)  # 父进程处理请求


if __name__ == '__main__':
    main()
