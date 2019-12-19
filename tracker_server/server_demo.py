import socket
import cv2
import numpy as np
from queue import Queue
from _thread import *
import time

enclosure_queue = Queue()


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)

    return buf


# 쓰레드 함수
def threaded(client_socket, addr, queue):
    recv = client_socket.recv(1024)
    print(recv)
    client_socket.send('ACK'.encode())

    while True:
        start = time.time()
        # length = recvall(client_socket, 16)
        # stringData = recvall(client_socket, int(length))
        stringData = recvall(client_socket, 691200)
        data = np.frombuffer(stringData, dtype='uint8')

        decimg = data.reshape(360, 640, 3)

        # decimg = cv2.imdecode(data, 1)

        print(type(data), len(data), "\n")

        # print(type(decimg), decimg.shape, "\n")

        cv2.imshow('Image', decimg)
        # cv2.waitKey(0)
        # print(int(length))
        # queue.put(stringData)

        key = cv2.waitKey(1)
        if key == 27:
            break

        print(time.time()-start)

# client_socket.send('ACK'.encode())

    client_socket.close()


HOST = '141.223.140.54'
PORT = 8888

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

print('server start')
print('wait')

client_socket, addr = server_socket.accept()
start_new_thread(threaded, (client_socket, addr, enclosure_queue,))

while True:
    pass

