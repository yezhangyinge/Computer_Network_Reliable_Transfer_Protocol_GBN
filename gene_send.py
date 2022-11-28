# Copyright (C) 2022 jiangzhijian, Inc. All Rights Reserved 
#
# @Time    : 11/18/2022 2:36 PM
# @Author  : jiangzhijian
# @File    : gene_send.py
# Do not change the content in this file!!

f = open("send.txt", "wb")
for i in range(0, 100):
    line = "-"*45 + f"{str(i):0>3s}\r\n"
    f.write(line.encode())
f.close()