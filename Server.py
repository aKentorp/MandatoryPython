from datetime import datetime, date
import socket
import time




# Create an UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



# input fra config
inputFromConfig = open('opt.conf').readlines()

input0 = inputFromConfig[0].split(':')
input1 = inputFromConfig[1].split(':')
input2 = inputFromConfig[2].split(':')
input3 = inputFromConfig[3].split(':')

heartBeat = bool(input0[1].replace('\n', ''))
maxPackagesPrSec = int(input1[1].replace('\n', ''))
reveiveBytes = int(input2[1].replace('\n', ''))
server_port = int(input3[1].replace('\n', ''))


# Bind the socket to the port
server_address = ('localhost', server_port)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
messageIncrement = 0;


# Kører indtil forced stop
while True:

    # 1. del af handshaket, hvor serveren modtager noget fra clienten
    print('\nwaiting to receive message')

    data, address = sock.recvfrom(reveiveBytes)
    data = data.decode()

    print(data)

    # tester om serveren modtager com-0 og gennemfører 2. del af handshaket
    if data == 'com-0':

        data = 'com-0 accept'.encode()
        sent = sock.sendto(data, address)
        print(data.decode())

        data, address = sock.recvfrom(reveiveBytes)
        data = data.decode()
        print(data)

        # Accepterer 3. del af handshaket og starter kommunikation mellem klient og server
        if data == 'com-0 accept':
            timeStart = datetime.now().time()

            while True:
                try:
                    sock.settimeout(None)
                    sock.settimeout(4)

                    data, address = sock.recvfrom(reveiveBytes)
                    data = data.decode()

                    if (data == 'con-h 0x00'):
                                print(data)
                                messageIncrement += 1

                                # test af time out funktionen
                                # hvis man sætter heartbeat til meget lavt
                                '''
                                timeNow = datetime.now().time()
                                testtest = datetime.combine(date.today(), timeNow) - datetime.combine(date.today(),
                                                                                                      timeStart)
                                testtesttest = messageIncrement / testtest.total_seconds()

                                if (testtesttest > maxPackagesPrSec):
                                    print("Client timed out for 2 sec")
                                    time.sleep(2)
                                '''
                    else:
                        print('msg-{}={}'.format(messageIncrement, data.encode()))
                        messageIncrement += 1

                        data = 'res-{}=I am server'.format(messageIncrement)
                        sent = sock.sendto(data.encode(), address)
                        print(data)

                        messageIncrement += 1

                        timeNow = datetime.now().time()
                        spamTimeBuffer = datetime.combine(date.today(), timeNow) - datetime.combine(date.today(), timeStart)
                        spamCheck = messageIncrement / spamTimeBuffer.total_seconds()

                        if (spamCheck > maxPackagesPrSec):
                            print("Client timed out for 2 sec")
                            time.sleep(2)



                except:
                    sock.settimeout(None)
                    print("Disconnected the client")

                    # Sender fejlmeddelsen
                    data = 'con-res 0xFE'.encode()
                    number = -1
                    sent = sock.sendto(data, address)

                    # Modtager et svar
                    data, address = sock.recvfrom(reveiveBytes)

                    print(data)
                    break

'''
while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)

    print('received {} bytes from {}'.format(len(data), address))
    print(data)

    if data:
        sent = sock.sendto(data, address)
        print('sent {} bytes back to {}'.format(sent, address))
'''

