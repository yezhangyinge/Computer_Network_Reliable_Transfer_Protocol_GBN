# receiver.py

import socket
import packet
import crc16
import UDT
import sys
import time
def receive(sock,filename,IP_PORT):
    UDTER = UDT.UDT(0.1,0.1)
    file = open(filename,"wb") 
    # ----------------------- log the message of receiving data ----------------------------
    log_filename = IP_PORT[0] + "_" + str(IP_PORT[1]) + "_" + "log_file.txt"
    log_file = open(log_filename,"a+")
    log_file.write("-------------------------------\n")
    log_file.write("Receiving %s...\n" %(filename))
    # --------------------------------------------------------------------------------------
    # ----------------------------- start GBN protocol -------------------------------------
    frame_expected = 0
    while True:
        pdu, addr = UDTER.recv(sock)      
        # get and extract packet
        if not pdu: 
            break
        seq_num, crc_num, data = packet.extract(pdu)
        # calc checksum
        crc_expected = crc16.crc16xmodem(data)
        # data corrupted
        if crc_expected != crc_num:
            log_file.write("%s: Receive PDU=%3d, STATUS=__CORRUPT__, FRAME_EXPECTED=%3d from %s\n" %(time.ctime(),seq_num,frame_expected,str(addr)))
            continue
        # data is good
        if seq_num==frame_expected:
            log_file.write("%s: Receive PDU=%3d, STATUS=____OK_____, FRAME_EXPECTED=%3d from %s\n" %(time.ctime(),seq_num,frame_expected,str(addr)))
            UDTER.sendack(frame_expected,sock,addr)
            frame_expected+=1
            file.write(data)
        # data does not have right sequence number 
        else:
            log_file.write("%s: Receive PDU=%3d, STATUS=__WRONGSEQ_, FRAME_EXPECTED=%3d from %s\n" %(time.ctime(),seq_num,frame_expected,str(addr)))
            UDTER.sendack(frame_expected-1,sock,addr)
    # ------------------------------------------------------------------------------------------
    print("over")
    log_file.write("Receive succeed\n")
    log_file.write("-------------------------------\n\n\n")
    log_file.close()
    file.close()

