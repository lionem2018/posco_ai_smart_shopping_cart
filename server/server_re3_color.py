import socket
import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import color_utils
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
isVerified = False
initialize = False
frameNum = 0
outputBoxToDraw = None
state_no_user = False
user_hsv_values = []

cluster_num = 3
threshold = 150
check_user_frame_num = 20
find_user_frame_num = 10

enclosure_queue = Queue()


# def on_mouse(event, x, y, flags, params):
#     global mousedown, mouseupdown, drawnBox, boxToDraw, initialize
#     if event == cv2.EVENT_LBUTTONDOWN:
#         drawnBox[[0,2]] = x
#         drawnBox[[1,3]] = y
#         mousedown = True
#         mouseupdown = False
#     elif mousedown and event == cv2.EVENT_MOUSEMOVE:
#         drawnBox[2] = x
#         drawnBox[3] = y
#     elif event == cv2.EVENT_LBUTTONUP:
#         drawnBox[2] = x
#         drawnBox[3] = y
#         mousedown = False
#         mouseupdown = True
#         initialize = True
#     boxToDraw = drawnBox.copy()
#     boxToDraw[[0,2]] = np.sort(boxToDraw[[0,2]])
#     boxToDraw[[1,3]] = np.sort(boxToDraw[[1,3]])




def track_in_image(img, mirror=False):
    global tracker, initialize, boxToDraw, outputBoxToDraw

    if mirror:
        img = cv2.flip(img, 1)
    # if mousedown:
    #     cv2.rectangle(img,
    #                   (int(boxToDraw[0]), int(boxToDraw[1])),
    #                   (int(boxToDraw[2]), int(boxToDraw[3])),
    #                   [0, 0, 255], PADDING)
    # elif mouseupdown:
    if isVerified:
        outputBoxToDraw = tracker.track('webcam', img[:, :, ::-1], boxToDraw)
        initialize = False
    else:
        outputBoxToDraw = tracker.track('webcam', img[:, :, ::-1])
        cv2.rectangle(img,
                      (int(outputBoxToDraw[0]), int(outputBoxToDraw[1])),
                      (int(outputBoxToDraw[2]), int(outputBoxToDraw[3])),
                      [0, 0, 255], PADDING)
    # cv2.imshow('Webcam', img)


def check_user(img, candidate_num, point_list):
    global boxToDraw, state_no_user

    user_id = -1
    user_bbox_left_top = np.zeros(2)
    user_bbox_right_low = np.zeros(2)
    pre_error_sum = 560
    pre_colors = user_hsv_values
    for person_num in range(candidate_num):
        point_left_top = point_list[2 * person_num]
        point_right_low = point_list[2 * person_num + 1]
        print(point_left_top, point_right_low)
        cropped_image = img[point_left_top[1]:point_right_low[1], point_left_top[0]:point_right_low[0]]
        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

        plt.figure()
        plt.axis("off")
        plt.imshow(cropped_image)

        # reshape the image to be a list of pixels
        cropped_image = cropped_image.reshape((cropped_image.shape[0] * cropped_image.shape[1], 3))

        # cluster the pixel intensities
        # clt = KMeans(n_clusters = args["clusters"])
        clt = KMeans(n_clusters=cluster_num)
        clt.fit(cropped_image)


        # build a histogram of clusters and then create a figure
        # representing the number of pixels labeled to each color
        hist = color_utils.centroid_histogram(clt)
        sorted_hist = np.sort(hist)[::-1]
        sorted_idx = np.argsort(sorted_hist)[::-1]
        bar = color_utils.plot_colors(sorted_hist, clt.cluster_centers_)

        # print(hist)
        # print(sorted_hist)
        # color = clt.cluster_centers_.astype('uint8')
        # color = np.array(clt.cluster_centers_, dtype=np.uint8)

        # colors 추출하여 hist의 값이 큰 순서로 colors 순서 바꾸기
        colors = clt.cluster_centers_.astype('uint8')
        sorted_colors = [colors[i] for i in sorted_idx]
        # print(colors)
        # print(sorted_colors)

        error_sum = 0
        # convert rgb color value to hsv
        for color_index, color in enumerate(sorted_colors):
            h_error = s_error = v_error = 0
            color = color_utils.rgb_to_hsv(color[0], color[1], color[2])
            # print(color_index, ":", color)

            # 유저 컬러 등록
            if len(user_hsv_values) < cluster_num:
                user_hsv_values.append(color)
                continue

            if user_hsv_values[color_index][0] > color[0]:
                if abs(user_hsv_values[color_index][0] - color[0]) < (360 - user_hsv_values[color_index][0] + color[0]):
                    h_error = user_hsv_values[color_index][0] - color[0]
                    # print("h error:", abs(user_hsv_values[color_index][0] - color[0]))
                else:
                    h_error = 360 - user_hsv_values[color_index][0] + color[0]
                    # print("h error:", 360 - user_hsv_values[color_index][0] + color[0])
            else:
                if abs(user_hsv_values[color_index][0] - color[0]) < (360 - color[0] + user_hsv_values[color_index][0]):
                    h_error = user_hsv_values[color_index][0] - color[0]
                    # print("h error:", abs(user_hsv_values[color_index][0] - color[0]))
                else:
                    h_error = 360 - color[0] + user_hsv_values[color_index][0]
                    # print("h error:", 360 - color[0] + user_hsv_values[color_index][0])

            s_error += user_hsv_values[color_index][1] - color[1]
            v_error += user_hsv_values[color_index][2] - color[2]

            # 컬러 면적별로 가중치 부여하여 error 누적
            if color_index == 0:
                error_sum += abs(h_error) + abs(s_error) + abs(v_error)
            elif color_index == 1:
                error_sum += (abs(h_error) + abs(s_error) + abs(v_error)) * 0.8
            else:
                error_sum += (abs(h_error) + abs(s_error) + abs(v_error)) * 0.4

            # 컬러별 그룹값 추출
            color_range = color_utils.hsv_to_color_range(color[0], color[1], color[2])
            # print(color_range)

        print("error_sum:", error_sum)

        if error_sum < threshold and error_sum < pre_error_sum:
            user_id = person_num
            user_bbox_left_top = point_left_top
            user_bbox_right_low = point_right_low
            pre_error_sum = error_sum
            pre_colors = sorted_colors

        # show our color bart
        plt.figure()
        plt.axis("off")
        plt.imshow(bar)
        plt.show()

    print("User:", user_id)

    # 사용자 컬러 정보 가중치 부여 저장 부분(확인필요)
    # if user_id != -1:
    #     for idx in range(cluster_num):
    #         user_hsv_values[idx][0] = user_hsv_values[idx][0] * 0.8 + pre_colors[idx][0] * 0.2
    #         user_hsv_values[idx][1] = user_hsv_values[idx][1] * 0.8 + pre_colors[idx][1] * 0.2
    #         user_hsv_values[idx][2] = user_hsv_values[idx][2] * 0.8 + pre_colors[idx][2] * 0.2
    #     print("update hsv: ", user_hsv_values)

    # 사용자의 위치 bbox 정보 수정
    # 사용자를 못찾으면 no user 상태로 변경하여 verifier가 더 자주 동작하도록 함
    if abs(user_bbox_left_top[0] - user_bbox_right_low[0]) > 0 and abs(user_bbox_left_top[1] - user_bbox_right_low[1]) > 0:
        boxToDraw[[0, 2]] = np.sort([user_bbox_left_top[0], user_bbox_right_low[0]])
        boxToDraw[[1, 3]] = np.sort([user_bbox_left_top[1], user_bbox_right_low[1]])
        state_no_user = False
    else:
        print("************* WARNING: Couldn't find user!! *************")
        state_no_user = True


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)

    return buf


# # 쓰레드 함수(main으로 빼둠)
# def threaded(client_socket, addr, queue):
#     global frameNum, isVerified, boxToDraw
#     recv = client_socket.recv(1024)
#     print(recv)
#     client_socket.send('ACK'.encode())
#
#     cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)
#     cv2.resizeWindow('Webcam', OUTPUT_WIDTH, OUTPUT_HEIGHT)
#     # cv2.setMouseCallback('Webcam', on_mouse, 0)
#
#     while True:
#         start = time.time()
#         # length = recvall(client_socket, 16)
#         # stringData = recvall(client_socket, int(length))
#         stringData = recvall(client_socket, 691200)
#         # stringData = recvall(client_socket, 93600)
#
#         candidate_num = recvall(client_socket, 5)
#         candidate_num = int(candidate_num)
#         point_data_len = recvall(client_socket, 5)
#         point_data_len = int(point_data_len)
#         stringPointData = recvall(client_socket, point_data_len)
#         angle_data_len = recvall(client_socket, 5)
#         angle_data_len = int(angle_data_len)
#         stringAngleData = recvall(client_socket, angle_data_len)
#
#         print("candidate_num: ", candidate_num)
#
#         data = np.frombuffer(stringData, dtype='uint8')
#         decimg = data.reshape(360, 640, 3)
#         # decimg = data.reshape(120, 260, 3)
#
#         # print(stringPointData)
#         point_list = ''
#         if point_data_len > 0:
#             point_list = list(ast.literal_eval(stringPointData.decode('utf-8')))
#         print("point_list: ", point_list)
#
#         # print(stringAngleData)
#         angle_list = ''
#         if angle_data_len > 0:
#             angle_list = list(ast.literal_eval(stringAngleData.decode('utf-8')))
#         print("angle_list: ", angle_list)
#
#         if frameNum % 20 == 0:
#             check_user(decimg, candidate_num, point_list)
#             isVerified = True
#         else:
#             track_in_image(decimg)
#             isVerified = False
#
#         # print(int(length))
#         # queue.put(stringData)
#
#         key = cv2.waitKey(1)
#         if key == 27:
#             break
#
#         frameNum += 1
#
#         print("[", frameNum, "], time:", time.time()-start)
#
# # client_socket.send('ACK'.encode())
#
#     client_socket.close()


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

    # main loop
    while True:
        recv = client_socket.recv(1024)
        print(recv)
        client_socket.send('ACK'.encode())

        cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Webcam', OUTPUT_WIDTH, OUTPUT_HEIGHT)
        # cv2.setMouseCallback('Webcam', on_mouse, 0)

        #
        while True:
            start = time.time()

            # client로 부터 데이터 받아오기
            # length = recvall(client_socket, 16)
            # stringData = recvall(client_socket, int(length))
            # 이미지 데이터 받아오기
            stringData = recvall(client_socket, 691200)
            # stringData = recvall(client_socket, 93600)

            # 유저 후보 수, 유저 후보 위치, 유저 후보 각도 정보 받아오기
            candidate_num = recvall(client_socket, 5)
            candidate_num = int(candidate_num)
            point_data_len = recvall(client_socket, 5)
            point_data_len = int(point_data_len)
            stringPointData = recvall(client_socket, point_data_len)
            angle_data_len = recvall(client_socket, 5)
            angle_data_len = int(angle_data_len)
            stringAngleData = recvall(client_socket, angle_data_len)
            distance_data_len = recvall(client_socket, 5)
            distance_data_len = int(distance_data_len)
            stringDistanceData = recvall(client_socket, distance_data_len)

            print("candidate_num: ", candidate_num)

            # 1차원 형태의 이미지 데이터 3차원으로 형태 변환
            data = np.frombuffer(stringData, dtype='uint8')
            decimg = data.reshape(360, 640, 3)
            # decimg = data.reshape(120, 260, 3)

            # bytes 형태의 point list 정보를 list로 변환
            # print(stringPointData)
            point_list = ''
            if point_data_len > 0:
                point_list = list(ast.literal_eval(stringPointData.decode('utf-8')))

            # 좌표값이 음수로 들어올 경우 0으로 지정
            for point in point_list:
                if point[0] < 0:
                    point[0] = 0
                elif point[1] < 0:
                    point[1] = 0

            print("point_list: ", point_list)

            # bytes 형태의 angle list 정보를 list로 변환
            # print(stringAngleData)
            angle_list = ''
            if angle_data_len > 0:
                angle_list = list(ast.literal_eval(stringAngleData.decode('utf-8')))
            print("angle_list: ", angle_list)

            # bytes 형태의 distance list 정보를 list로 변환
            # print(stringDistanceData)
            distance_list = ''
            if distance_data_len > 0:
                distance_list = list(ast.literal_eval(stringDistanceData.decode('utf-8')))
            print("distance_list: ", distance_list)

            # # 20 프레임마다 verifier 작동(color 확인)
            # if frameNum % 20 == 0:
            #     check_user(decimg, candidate_num, point_list)
            #     isVerified = True
            # else:
            #     if not state_no_user:
            #         track_in_image(decimg)
            #         isVerified = False

            if not state_no_user:
                if frameNum % check_user_frame_num == 0:
                    check_user(decimg, candidate_num, point_list)
                    isVerified = True
                else:
                    track_in_image(decimg)
                    isVerified = False
            else:
                if frameNum % find_user_frame_num == 0:
                    check_user(decimg, candidate_num, point_list)
                    if not state_no_user:
                        isVerified = True

            cv2.imshow('Webcam', decimg)

            # print(int(length))
            # queue.put(stringData)

            key = cv2.waitKey(1)
            if key == 27:
                break

            frameNum += 1

            print("[", frameNum, "], time:", time.time() - start, "===========================")



