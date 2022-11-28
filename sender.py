#sender.py

import socket
import PDU
import UDT
import _thread
import timer
import sys
import packet
import crc16
import time
import threading
interval=1


base = 0      
num_packets = 0  
send_timer = timer.timer(interval)  
log_filename = ""
mutex = _thread.allocate_lock()  
UDTER = UDT.UDT(0.1,0.1)   
def send(sock,filename,IP_PORT,RECEIVER_ADDR):
    global UDTER  
    global mutex  
    global base  
    global num_packets   
    global send_timer    
    global log_filename 
    # ----------------------- log the message of sending data ----------------------------
    send_IP = IP_PORT[0]        
    send_PORT = str(IP_PORT[1]) 
    recv_IP = RECEIVER_ADDR[0]  
    recv_PORT = str(RECEIVER_ADDR[1])  
    log_filename = send_IP+"_"+send_PORT+"_"+"log_file.txt"
    log_file = open(log_filename,"a+")
    file = open(filename,"rb")
    log_file.write("-------------------------------\n")
    log_file.write(f"{send_IP + ':' + send_PORT} send {filename} to {recv_IP+ ':' + recv_PORT}")
    # ------------------------------------------------------------------------------------
    # ----------------------------- create sending buffer --------------------------------
    packets = [] 
    seq_num = 0
    while True:
        data = file.read(50)    
        if not data:  
            break
        crc_num = crc16.crc16xmodem(data)  
        pdu = packet.make(seq_num,crc_num,data)  
        packets.append(pdu)  
        seq_num += 1  
    num_packets = len(packets)  
    log_file.write("total %d packets\n" %(num_packets))  
    print('I gots', num_packets)
    # --------------------------------------------------------------------------------------
    # ----------------------------- start GBN protocol -------------------------------------
    N = 30  # window size
    next_seqnum = 0
    THREAD = threading.Thread(target=receive,args=(sock,))
    THREAD.start()
    timeout = 0
    scale = 50
    start = time.perf_counter()  
    pre = start
    while base < num_packets:
        mutex.acquire()  
        while next_seqnum < base + N:
            # do not exceed total packets
            if next_seqnum >= num_packets:
                break
            # log the sending data
            if timeout == 0:
                log_file.write("%s: Send PDU=%3d, STATUS=__SEND__, ACKed=%3d to %s\n" % (time.ctime(),next_seqnum,base,str(RECEIVER_ADDR)))
            # log the resending data
            elif timeout == 1:
                log_file.write("%s: Send PDU=%3d, STATUS=_RESEND_, ACKed=%3d to %s\n" % (time.ctime(),next_seqnum,base,str(RECEIVER_ADDR)))
            UDTER.send(packets[next_seqnum], sock, RECEIVER_ADDR)
            send_timer.start(next_seqnum)  
            next_seqnum += 1
        timeout = 0
        if send_timer.overtime(base): 
            # log timeout
            log_file.write(f"{time.ctime()}: Send PDU={base:3d}  is timeout, need to resend to {str(RECEIVER_ADDR)}!!!!!!!!!!!!!!!\n")
            timeout = 1
            next_seqnum = base
        
        if (time.perf_counter() - pre) > 1:
            pre = time.perf_counter()  
            param = (int) (num_packets/50)
            i = (int) (next_seqnum/param)
            a = '*' * i 
            b = '.' * (scale-i) 
            c = (i/scale) * 100
            duration = pre - start
            print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c,a,b,duration),end='')
        mutex.release()
    log_file.write("%s: Send PDU=%3d, STATUS=_FINISH_, ACKed=%3d to %s\n" % (time.ctime(),next_seqnum-1,base,str(RECEIVER_ADDR)))
    print("\nover")
    UDTER.send(packet.make_empty(), sock, RECEIVER_ADDR) 
    log_file.write("send succeed\n") 
    log_file.write("-------------------------------\n\n\n")
    file.close()
    log_file.close()

def receive(sock):

    global mutex
    global base
    global num_packets
    
    while True:
        # get the ack 
        ack, _ = UDTER.recvack(sock)
        # use the ack to update "base"
        if ack >= base:
            mutex.acquire()
            base = ack + 1
            mutex.release()
        if base >= num_packets:
            break

