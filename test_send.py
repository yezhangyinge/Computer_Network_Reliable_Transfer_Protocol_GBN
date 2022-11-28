# Copyright (C) 2022 jiangzhijian, Inc. All Rights Reserved 
#
# @Time    : 11/18/2022 2:36 PM
# @Author  : jiangzhijian
# @File    : test_send.py
# Do not change the content in this file!!

import sender
import receiver
import socket
import sys
import threading

def main():
    # sender IP
    IP="127.0.0.1"
    PORT=8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP_PORT=(IP,PORT)
    sock.bind(IP_PORT) 
    # test
    while(True):
        option=input("Please input your option: send/receive/close: ")
        if option=="send":
            lock=threading.Lock()
            lock.acquire()
            filename="./send.txt"
            RECEIVER_IP="127.0.0.1"
            RECEIVER_PORT=9090
            RECEIVER_IP_PORT=(RECEIVER_IP,RECEIVER_PORT)
            lock.release()
            
            send_thread=threading.Thread(target=sender.send,args=(sock,filename,IP_PORT,RECEIVER_IP_PORT))
            send_thread.start()
            send_thread.join()
        elif option=="close":
            sock.close()
            break
        else:
            continue

if __name__=='__main__':
    main()
