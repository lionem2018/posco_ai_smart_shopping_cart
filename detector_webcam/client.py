import socket
import numpy as np
import cv2
from queue import Queue
from _thread import *
import time

enclosure_queue = Queue()
# 보연이 workstation 에 세팅
HOST ='141.223.140.53'
# HOST = '127.0.0.1'
PORT = 8888

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def webcam(queue):
    capture = cv2.VideoCapture(2)
    capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)

    while True:
        time.sleep(0.1)
        ret, frame = capture.read()

        if ret == False:
            continue

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)

        data = np.array(imgencode)
        stringData = data.tostring()

        queue.put(stringData)

        # cv2.imshow('image', frame)
        #time.sleep(0.1)



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


# 비디오 캡쳐 객체를 생성할 수 있음. 안의 숫자는 장치 인덱스(어떤 카메라를 사용할가)
# 1개만 부착되어 있으면 0
# 비디오의 한 프레임씩 읽어옴


print("Conneted!")

client_socket.send('3;CAM'.encode())
# time.sleep(0.2)
start_new_thread(webcam, (enclosure_queue,))
print('while start')
while True:
# pass
    data = client_socket.recv(10)
    stringData = enclosure_queue.get()
    client_socket.send(str(len(stringData)).ljust(16).encode())
    client_socket.send(stringData)

    key = cv2.waitKey(1)
    if key == 27:
        break



# capture.release()
client_socket.close()

