import socket
import cv2
import numpy as np
from queue import Queue
from _thread import *
import time

enclosure_queue = Queue()
CMD_STOP = "S,0;S,0;S,0;S,0;N"

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def communication_cart(client_socket, queue):
    cmd = CMD_STOP
    print('comm cart start!')
    client_socket.send(cmd.encode())
    while True:
        recv_packet = client_socket.recv(1024).decode()
        print(recv_packet)
        queue_cmd = queue.get()
        cmd = queue_cmd

        if queue_cmd == '':
            client_socket.send(CMD_STOP.encode())
        else:
            client_socket.send(cmd.encode())

    client_socket.close()

def manual_control_cart(queue):
    while True:
        keyboard_input = input("\r\n>> ")
        # speed ratio check motor1,2(100=80rpm) <--> motor3,4(100=130rpm)
        if keyboard_input == 'CO':  # check OK
            queue.put('S,0;S,0;S,0;S,0;G')
        elif keyboard_input == 'CE':  # check Error
            queue.put('S,0;S,0;S,0;S,0;B')
        elif keyboard_input == 'E':  # just for test(maybe do not use), ultrasonic sensor will turn on red light
            queue.put('S,0;S,0;S,0;S,0;R')
        elif keyboard_input == 'S':
            queue.put('S,0;S,0;S,0;S,0;N')
        elif keyboard_input == 'F':
            queue.put('F,100;F,100;F,100;F,100;N')
        elif keyboard_input == 'B':
            queue.put('B,100;B,100;B,100;B,100;N')
        elif keyboard_input == 'R1':
            queue.put('F,100;F,100;F,80;F,100;N')
        elif keyboard_input == 'R2':
            queue.put('F,100;F,100;F,60;F,100;N')
        elif keyboard_input == 'R3':
            queue.put('F,100;F,100;F,40;F,100;N')
        elif keyboard_input == 'R4':
            queue.put('F,100;F,100;F,20;F,100;N')
        elif keyboard_input == 'L1':
            queue.put('F,100;F,100;F,100;F,80;N')
        elif keyboard_input == 'L2':
            queue.put('F,100;F,100;F,100;F,60;N')
        elif keyboard_input == 'L3':
            queue.put('F,100;F,100;F,100;F,40;N')
        elif keyboard_input == 'L4':
            queue.put('F,100;F,100;F,100;F,20;N')

def wait_accept_socket(server_socket, queue):
    while True:
        client_socket, addr = server_socket.accept()
        recv_packet = client_socket.recv(1024).decode()
        print('connected client')

        if recv_packet == '1;CART':
            print('connected CART!!')
            start_new_thread(communication_cart, (client_socket, queue,))
            start_new_thread(manual_control_cart, (queue,))

HOST = '141.223.140.46'
PORT = 8888

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

print('server start')
num_connected = 0

while True:
    client_socket, addr = server_socket.accept()
    recv_packet = client_socket.recv(1024).decode()
    print(recv_packet)

    if recv_packet == '1;CART':
        start_new_thread(communication_cart, (client_socket, enclosure_queue,))
        start_new_thread(manual_control_cart, (enclosure_queue,))
    elif recv_packet == '2;AZURE':
        start_new_thread(wait_accept_socket, (server_socket, enclosure_queue,))
        break

while True:
    # 여기에 AZURE 수신 한 뒤 Re3 부분 추가
    # 거리, 각도 값에 따라 모터 명령 코드를 추가
    # 모터 명령을 enclosure_queue에 put 한다(manual_control_cart 함수 참고)
    pass










