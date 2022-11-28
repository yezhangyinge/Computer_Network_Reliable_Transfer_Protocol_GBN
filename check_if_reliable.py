# Copyright (C) 2022 jiangzhijian, Inc. All Rights Reserved 
#
# @Time    : 11/18/2022 2:36 PM
# @Author  : jiangzhijian
# @File    : check_if_reliable.py
# Do not change the content in this file!!

import hashlib

def get_file_md5(f):
    m = hashlib.md5()
    while True:
        data = f.read(1024) # get chunk
        if not data:
            break
        m.update(data)
    return m.hexdigest()


send_f = open("./send.txt", "rb")
recv_f = open("./recv.txt", "rb")
send_f_md5 = get_file_md5(send_f)
recv_f_md5 = get_file_md5(recv_f)
if send_f_md5 != recv_f_md5:
    print(f"You do not create Reliable Transmission!!")
else:
    print(f"You get the same data using Reliable Transmission")