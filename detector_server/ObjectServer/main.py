import socket, sys
import cv2
import numpy as np
from _thread import *
from time import time as timer
from queue import Queue
from darkflow.defaults import argHandler #Import the default arguments
from darkflow.net.build import TFNet

enclosure_queue_img = Queue()
enclosure_queue_labels = Queue()

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def communication_with_monitor(client_socket, queue_img, queue_labels):

    print('thread start!!')

    while not queue_img.empty():
        print("queue_img")
        queue_img.get()

    while not queue_labels.empty():
        print("queue_labels")
        queue_labels.get()

    while True:
        print("while start")
        try:
            # stringData = queue.get()
            # client_socket.send(str(len(stringData)).ljust(16).encode())
            # print(stringData[0:5])

            dataString = queue_img.get()
            print(len(dataString))
            # client_socket.send(str(len(dataString)).ljust(16).encode())
            # send image
            # client_socket.send(str(len(dataString)).ljust(16).encode())
            client_socket.send(dataString)
            # get dummy
            data = client_socket.recv(10)
            print("recv1")
            # send label_list
            labels_list = queue_labels.get()
            client_socket.send(labels_list.encode())
            data = client_socket.recv(10)
            print("recv2")

        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0], ':', addr[1])
            break

    client_socket.close()


args = ['./flow', '--model', '../cfg/tiny-yolo-voc-24c.cfg', '--load', '127928', '--client_camera', 'True', '--gpu', '1.0']

# HOST = '127.0.0.1'
HOST = '141.223.140.53'
PORT = 8888

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

is_connected_showCli = False

num_connected_cli = 0

while True:

    client_socket, addr = server_socket.accept()
    recv_packet = client_socket.recv(1024).decode()
    if recv_packet == '3;CAM':
        num_connected_cli = num_connected_cli + 1
        print("CAM connected")
        break

    elif recv_packet == '4;MONITOR':
        is_connected_showCli = True
        start_new_thread(communication_with_monitor, (client_socket, enclosure_queue_img, enclosure_queue_labels))
        num_connected_cli = num_connected_cli + 1
        print("MONITOR connected")

    if num_connected_cli > 1 : break

print('Start')

FLAGS = argHandler()
FLAGS.setDefaults()
FLAGS.parseArgs(args)
tfnet = TFNet(FLAGS)
print(FLAGS)

while True:
    message = '1'
    client_socket.send(message.encode())

    length = recvall(client_socket, 16)
    stringData = recvall(client_socket, int(length))
    data = np.frombuffer(stringData, dtype='uint8')

    frame = cv2.imdecode(data, 1)
    # cv2.imshow('Image', decimg)

    # 외부로 빼야 함
    # cv2.namedWindow('', 0)
    # height, width, _ = frame.shape
    # cv2.resizeWindow('', width, height)

    # buffers for demo in batch
    buffer_inp = list()
    buffer_pre = list()

    elapsed = int()
    start = timer()

    elapsed += 1
    if frame is None:
        exit('\nEnd of Video')

    preprocessed = tfnet.framework.preprocess(frame)
    buffer_inp.append(frame)
    buffer_pre.append(preprocessed)

    # stringData = ''
    # Only process and imshow when queue is full
    if elapsed % tfnet.FLAGS.queue == 0:
        feed_dict = {tfnet.inp: buffer_pre}
        net_out = tfnet.sess.run(tfnet.out, feed_dict)
        for img, single_out in zip(buffer_inp, net_out):
            postprocessed, labels_list = tfnet.framework.postprocess_for_client(single_out, img, False)

            print(postprocessed.shape)
            print(np.array(postprocessed).tostring()[0:5])
            while not enclosure_queue_img.empty():
                continue
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, imgencode = cv2.imencode('.jpg', postprocessed, encode_param)
            data = np.array(imgencode)
            stringData = data.tostring()
            enclosure_queue_img.put(stringData)
            print(stringData[0:5])

            while not enclosure_queue_labels.empty():
                continue

            enclosure_queue_labels.put(str(labels_list))
            # cv2.imshow('', postprocessed)
            print(labels_list)
        # Clear Buffers
        buffer_inp = list()
        buffer_pre = list()


    # imshow 를 지우고 받은 데이터를 가지고 Object Detection
    # 검출결과를 monitor client에게 전송
    # if is_connected_showCli:
    #     enclosure_queue.put(stringData)
    # else:
    #     pass

    key = cv2.waitKey(1)
    if key == 27:
        break

    sys.stdout.write('\n')

client_socket.close()
