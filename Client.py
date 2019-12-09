from datetime import datetime, date
import socket
import time
from threading import *

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class HeartBeatClass(Thread):

    def run(self):
        while heartBeat:
        # while heartBeat == 'True':

            time.sleep(3)
            heartBeatMessage = 'con-h 0x00'
            sentHeartBeat = sock.sendto(heartBeatMessage.encode(), server_address)

            # print('badump')

# Få og sæt input fra config filen
inputFromConfig = open('opt.conf').readlines()

input0 = inputFromConfig[0].split(':')
input1 = inputFromConfig[1].split(':')
input2 = inputFromConfig[2].split(':')
input3 = inputFromConfig[3].split(':')

heartBeat = bool(input0[1].replace('\n', ''))
maxPackagesPrSec = int(input1[1].replace('\n', ''))
reveiveBytes = int(input2[1].replace('\n', ''))
server_port = int(input3[1].replace('\n', ''))

server_address = ('localhost', server_port)


try:

    # 3-way handshake
    sent = sock.sendto('com-0'.encode(), server_address)

    receiveMsg, server_address = sock.recvfrom(reveiveBytes)
    receiveMsg = receiveMsg.decode()
    print(receiveMsg)

    if receiveMsg == 'com-0 accept':

        sent = sock.sendto('com-0 accept'.encode(), server_address)

        thread1 = HeartBeatClass()
        thread1.start()

        while True:


            message = input()
            sent = sock.sendto(message.encode(), server_address)

            receiveMsg, server_address = sock.recvfrom(reveiveBytes)
            receiveMsg = receiveMsg.decode()

            if receiveMsg == 'con-res 0xFE':
                sent = sock.sendto('con-res x0FF'.encode, server_address)
                break
            elif receiveMsg:
                print(receiveMsg.split('=')[1])



finally:
    heartBeat = False
    thread1.join()
    sock.close()

