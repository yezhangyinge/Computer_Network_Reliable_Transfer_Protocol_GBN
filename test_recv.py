# Copyright (C) 2022 jiangzhijian, Inc. All Rights Reserved 
#
# @Time    : 11/18/2022 2:36 PM
# @Author  : jiangzhijian
# @File    : test_recv.py
# Do not change the content in this file!!

import sender
import receiver
import socket
import sys
import threading

def main():
    # receiver IP
    IP="127.0.0.1"
    PORT=9090
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP_PORT=(IP,PORT)
    sock.bind(IP_PORT) 
    # test
    while(True):
        option=input("Please input your option: send/receive/close: ")
        if option=="receive":
            lock=threading.Lock()
            lock.acquire()
            filename="./recv.txt"
            lock.release()
            receive_thread=threading.Thread(target=receiver.receive,args=(sock,filename,IP_PORT))
            receive_thread.start()
            receive_thread.join()
        elif option=="close":
            sock.close()
            break
        else:
            continue

if __name__=='__main__':
    main()
