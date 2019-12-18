"""
chat room client
"""
from socket import *
import os,sys

# 服务器地址
ADDR = ('127.0.0.1',8888)

# 发送消息
def send_msg(s,name):
    while True:
        try:
            text = input("Msg>>")
        except KeyboardInterrupt:
            text = 'quit'
        # 退出
        if text == 'quit':
            msg = "Q "+name
            s.sendto(msg.encode(),ADDR)
            sys.exit("退出群聊")
        msg = "C %s %s"%(name,text)
        s.sendto(msg.encode(),ADDR)

# 接收消息
def recv_msg(s):
    while True:
        try:
            data,addr = s.recvfrom(4096)
        except KeyboardInterrupt:
            sys.exit()
        if data == b'EXIT':
            sys.exit()
        print(data.decode()+'\nMsg>>',end='')

# 客户端启动函数
def main():
    s = socket(AF_INET,SOCK_DGRAM)
    # 进入聊天室部分
    while True:
        name = input("请输入姓名:")
        msg = "L "+name
        s.sendto(msg.encode(),ADDR)
        # 得到结果
        data,addr = s.recvfrom(128)
        if data.decode() == 'OK':
            print("您已进入聊天室")
            break
        else:
            print('进入聊天室失败')

    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        send_msg(s,name) # 子进程发送
    else:
        recv_msg(s) # 父进程接收


if __name__ == '__main__':
    main()