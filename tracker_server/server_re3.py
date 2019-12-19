import socket
import cv2
import numpy as np
from queue import Queue
from _thread import *
import time, glob
import argparse
import os, sys, ast

basedir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basedir, os.path.pardir)))
from tracker import re3_tracker

from constants import OUTPUT_WIDTH
from constants import OUTPUT_HEIGHT
from constants import PADDING

np.set_printoptions(precision=6)
np.set_printoptions(suppress=True)

drawnBox = np.zeros(4)
boxToDraw = np.zeros(4)
mousedown = False
mouseupdown = False
initialize = False
frameNum = 0

enclosure_queue = Queue()


def on_mouse(event, x, y, flags, params):
    global mousedown, mouseupdown, drawnBox, boxToDraw, initialize
    if event == cv2.EVENT_LBUTTONDOWN:
        drawnBox[[0,2]] = x
        drawnBox[[1,3]] = y
        mousedown = True
        mouseupdown = False
    elif mousedown and event == cv2.EVENT_MOUSEMOVE:
        drawnBox[2] = x
        drawnBox[3] = y
    elif event == cv2.EVENT_LBUTTONUP:
        drawnBox[2] = x
        drawnBox[3] = y
        mousedown = False
        mouseupdown = True
        initialize = True
    boxToDraw = drawnBox.copy()
    boxToDraw[[0,2]] = np.sort(boxToDraw[[0,2]])
    boxToDraw[[1,3]] = np.sort(boxToDraw[[1,3]])


def track_in_image(img, mirror=False):
    global tracker, initialize, frameNum

    if mirror:
        img = cv2.flip(img, 1)
    if mousedown:
        cv2.rectangle(img,
                      (int(boxToDraw[0]), int(boxToDraw[1])),
                      (int(boxToDraw[2]), int(boxToDraw[3])),
                      [0, 0, 255], PADDING)
    elif mouseupdown:
        if initialize:
            outputBoxToDraw = tracker.track('webcam', img[:, :, ::-1], boxToDraw)
            initialize = False
        else:
            outputBoxToDraw = tracker.track('webcam', img[:, :, ::-1])
        cv2.rectangle(img,
                      (int(outputBoxToDraw[0]), int(outputBoxToDraw[1])),
                      (int(outputBoxToDraw[2]), int(outputBoxToDraw[3])),
                      [0, 0, 255], PADDING)
    cv2.imshow('Webcam', img)
    frameNum += 1


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

    cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Webcam', OUTPUT_WIDTH, OUTPUT_HEIGHT)
    cv2.setMouseCallback('Webcam', on_mouse, 0)

    while True:
        start = time.time()
        # length = recvall(client_socket, 16)
        stringData = recvall(client_socket, 93600)
        # stringData = bytes(client_socket.recv(93600))

        candidate_num = recvall(client_socket, 5)
        candidate_num = int(candidate_num)
        point_data_len = recvall(client_socket, 5)
        point_data_len = int(point_data_len)
        stringPointData = recvall(client_socket, point_data_len)
        angle_data_len = recvall(client_socket, 5)
        angle_data_len = int(angle_data_len)
        stringAngleData = recvall(client_socket, angle_data_len)

        # print(candidate_num)
        #
        data = np.frombuffer(stringData, dtype='uint8')
        decimg = data.reshape(120, 260, 3)
        # decimg = data.reshape(120, 260, 3)

        print(stringPointData)
        point_list = ''
        if point_data_len > 0:
            point_list = list(ast.literal_eval(stringPointData.decode('utf-8')))
        print(point_list)

        print(stringAngleData)
        angle_list = ''
        if angle_data_len > 0:
            angle_list = list(ast.literal_eval(stringAngleData.decode('utf-8')))
        print(angle_list)

        track_in_image(decimg)

        # print(int(length))
        # queue.put(stringData)

        # cv2.imshow('Webcam', decimg)
        key = cv2.waitKey(1)
        if key == 27:
            break

        print(frameNum, time.time()-start)

# client_socket.send('ACK'.encode())

    client_socket.close()


HOST = '141.223.140.54'
PORT = 8888

# Main function
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Show the Webcam demo.')
    args = parser.parse_args()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print('server start')
    print('wait')

    tracker = re3_tracker.Re3Tracker()

    client_socket, addr = server_socket.accept()
    # start_new_thread(threaded, (client_socket, addr, enclosure_queue,))

    while True:
        # pass
        recv = client_socket.recv(1024)
        print(recv)
        client_socket.send('ACK'.encode())

        cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Webcam', OUTPUT_WIDTH, OUTPUT_HEIGHT)
        cv2.setMouseCallback('Webcam', on_mouse, 0)

        while True:
            start = time.time()
            # length = recvall(client_socket, 16)
            stringData = recvall(client_socket, 691200)
            # stringData = bytes(client_socket.recv(93600))

            candidate_num = recvall(client_socket, 5)
            candidate_num = int(candidate_num)
            point_data_len = recvall(client_socket, 5)
            point_data_len = int(point_data_len)
            stringPointData = recvall(client_socket, point_data_len)
            angle_data_len = recvall(client_socket, 5)
            angle_data_len = int(angle_data_len)
            stringAngleData = recvall(client_socket, angle_data_len)

            # print(candidate_num)
            #
            data = np.frombuffer(stringData, dtype='uint8')
            decimg = data.reshape(360, 640, 3)
            # decimg = data.reshape(120, 260, 3)

            print(stringPointData)
            point_list = ''
            if point_data_len > 0:
                point_list = list(ast.literal_eval(stringPointData.decode('utf-8')))
            print(point_list)

            print(stringAngleData)
            angle_list = ''
            if angle_data_len > 0:
                angle_list = list(ast.literal_eval(stringAngleData.decode('utf-8')))
            print(angle_list)

            track_in_image(decimg)

            # print(int(length))
            # queue.put(stringData)

            # cv2.imshow('Webcam', decimg)
            key = cv2.waitKey(1)
            if key == 27:
                break

            print(frameNum, time.time() - start)
