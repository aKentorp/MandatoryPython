import socket


# Hacket lader serveren hænge i første del af handshaket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)


try:
    message1 = 'com-0'

    sent = sock.sendto(message1.encode(), server_address)


finally:
    print('closing socket')
    heartbeat = False
    sock.close()
