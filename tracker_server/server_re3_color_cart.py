import socket
import cv2
import numpy as np
from queue import Queue
from _thread import *
import time
from sklearn.cluster import KMeans
import color_utils
import os, sys, ast
from datetime import datetime
import constants
import matplotlib.pyplot as plt

basedir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basedir, os.path.pardir)))
from tracker import re3_tracker

from constants import OUTPUT_WIDTH
from constants import OUTPUT_HEIGHT
from constants import PADDING

np.set_printoptions(precision=6)
np.set_printoptions(suppress=True)

CMD_STOP = "S,0;S,0;S,0;S,0;N"

HOST = '141.223.140.54'
PORT = 8888

drawnBox = np.zeros(4)
boxToDraw = np.zeros(4)
isVerified = False
initialize = False
frameNum = 0
outputBoxToDraw = None
state_no_user = False
not_found_count = 0

wheel1_speed = 0
wheel2_speed = 0
wheel3_speed = 0
wheel4_speed = 0
motor_control = ''

# 유저의 컬러 값 저장 리스트
user_hsv_values = []
# verifier가 판단한 유저의 아이디
user_id = -1

enclosure_queue = Queue()


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
        print(recv_packet, datetime.now())
        queue_cmd = queue.get()
        cmd = queue_cmd
        if queue_cmd == '':
            client_socket.send(CMD_STOP.encode())
        else:
            client_socket.send(cmd.encode())

    client_socket.close()


def test_cart_input(queue):
    cmd = CMD_STOP
    print('comm cart start!')
    while True:
        queue_cmd = queue.get()
        cmd = queue_cmd

        if queue_cmd == '':
            print(CMD_STOP)
        else:
            print(cmd)


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


def track_in_image(img, mirror=False):
    global tracker, initialize, boxToDraw, outputBoxToDraw

    if mirror:
        img = cv2.flip(img, 1)

    if isVerified:
        outputBoxToDraw = tracker.track('webcam', img[:, :, ::-1], boxToDraw)
        initialize = False
    else:
        outputBoxToDraw = tracker.track('webcam', img[:, :, ::-1])
        cv2.rectangle(img,
                      (int(outputBoxToDraw[0]), int(outputBoxToDraw[1])),
                      (int(outputBoxToDraw[2]), int(outputBoxToDraw[3])),
                      [0, 0, 255], PADDING)


def check_user(img, candidate_num, point_list):
    global boxToDraw, state_no_user, user_id

    user_id = -1
    user_bbox_left_top = np.zeros(2)
    user_bbox_right_low = np.zeros(2)
    pre_error_sum = 560
    pre_colors = user_hsv_values
    for person_num in range(candidate_num):
        point_left_top = point_list[2 * person_num]
        point_right_low = point_list[2 * person_num + 1]

        # print(point_left_top, point_right_low)
        cropped_image_original = img[point_left_top[1]:point_right_low[1], point_left_top[0]:point_right_low[0]]
        cropped_image = cv2.cvtColor(cropped_image_original, cv2.COLOR_BGR2RGB)

        ####################################################################
        bbox_width = cropped_image.shape[1]
        bbox_height = cropped_image.shape[0]

        point_color_top = cropped_image[int(bbox_height / 6)][int(bbox_width / 3.5)]
        # print(int(bbox_height / 6), int(bbox_width / 3.5), point_color_top)
        point_color_bottom = cropped_image[int(bbox_height / 6 * 5)][int(bbox_width / 3.5 * 2.5)]
        # print(int(bbox_height / 6 * 5), int(bbox_width / 3.5 * 2.5), point_color_top)

        # 색상 기준 6 좌표 추출
        cv2.circle(cropped_image_original, (int(bbox_width / 3.5), int(bbox_height / 6)), 2, (0, 0, 255), -1)
        # cv2.circle(cropped_image, (int(bbox_height / 3.5 * 2.5), int(bbox_width / 6 * 3)), 1, (255, 0, 0), -1)
        # cv2.circle(cropped_image, (int(bbox_height / 3.5), int(bbox_width / 6 * 5)), 1, (255, 0, 0), -1)
        # cv2.circle(cropped_image, (int(bbox_height / 3.5 * 2.5), int(bbox_width / 6)), 1, (255, 0, 0), -1)
        # cv2.circle(cropped_image, (int(bbox_height / 3.5), int(bbox_width / 6 * 3)), 1, (255, 0, 0), -1)
        cv2.circle(cropped_image_original, (int(bbox_width / 3.5 * 2.5), int(bbox_height / 6 * 5)), 2, (0, 0, 255), -1)

        #############################################################################
        # reshape the image to be a list of pixels
        cropped_image = cropped_image.reshape((cropped_image.shape[0] * cropped_image.shape[1], 3))

        clt = KMeans(n_clusters=constants.CLUSTER_NUM, init='k-means++')
        # clt = KMeans(n_clusters=CLUSTER_NUM)
        clt.fit(cropped_image)

        # build a histogram of clusters and then create a figure
        # representing the number of pixels labeled to each color
        hist = color_utils.centroid_histogram(clt)
        sorted_hist = np.sort(hist)[::-1]
        sorted_idx = np.argsort(sorted_hist)[::-1]
        bar = color_utils.plot_colors(sorted_hist, clt.cluster_centers_)

        # colors 추출하여 hist의 값이 큰 순서로 colors 순서 바꾸기
        colors = clt.cluster_centers_.astype('uint8')
        sorted_colors = [colors[i] for i in sorted_idx]

        ###################################################
        print("비교대상: ", point_color_top, point_color_bottom)
        print("sorted_color:", [sorted_colors])

        clust_colors = []
        clust_num = -1
        pre_e = pow(560, 2)

        for i in range(constants.CLUSTER_NUM):
            e = 0
            for c in range(3):
                e += pow(int(sorted_colors[i][c]) - int(point_color_top[c]), 2)

            if e < pre_e:
                pre_e = e
                clust_num = i

        clust_colors.append(sorted_colors[clust_num])

        clust_num = -1
        pre_e = pow(560, 2)

        for i in range(constants.CLUSTER_NUM):
            e = 0
            for c in range(3):
                e += pow(int(sorted_colors[i][c]) - int(point_color_bottom[c]), 2)

            if e < pre_e:
                pre_e = e
                clust_num = i

        clust_colors.append(sorted_colors[clust_num])

        print("clust colors: ", clust_colors)
        ####################################################

        error_sum = 0
        # convert rgb color value to hsv
        for color_index, color in enumerate(clust_colors):
            h_error = s_error = v_error = 0
            color = color_utils.rgb_to_hsv(color[0], color[1], color[2])

            # 유저 컬러 등록
            if len(user_hsv_values) < constants.CLUSTER_NUM - 1:
                user_hsv_values.append(color)
                continue

            if user_hsv_values[color_index][0] > color[0]:
                if abs(user_hsv_values[color_index][0] - color[0]) < (360 - user_hsv_values[color_index][0] + color[0]):
                    h_error = user_hsv_values[color_index][0] - color[0]
                else:
                    h_error = 360 - user_hsv_values[color_index][0] + color[0]
            else:
                if abs(user_hsv_values[color_index][0] - color[0]) < (360 - color[0] + user_hsv_values[color_index][0]):
                    h_error = user_hsv_values[color_index][0] - color[0]
                else:
                    h_error = 360 - color[0] + user_hsv_values[color_index][0]

            s_error = user_hsv_values[color_index][1] - color[1]
            v_error = user_hsv_values[color_index][2] - color[2]

            print(user_hsv_values[color_index], "-----", color)
            print("[", person_num, "]", "h_error:", abs(h_error), "|| s_error:", abs(s_error), "|| v_error:", abs(v_error))

            # 컬러 면적별로 가중치 부여하여 error 누적
            if color_index == 0:
                error_sum += abs(h_error) + abs(s_error) + abs(v_error)
            elif color_index == 1:
                error_sum += (abs(h_error) + abs(s_error) + abs(v_error)) * 0.8
            else:
                error_sum += (abs(h_error) + abs(s_error) + abs(v_error)) * 0.4

            # 컬러별 그룹값 추출
            # color_range = color_utils.hsv_to_color_range(color[0], color[1], color[2])

        print("[", person_num, "] error_sum:", error_sum)

        # if h_error < H_COLOR_THRESHOLD and s_error < S_COLOR_THRESHOLD and error_sum < TOTAL_COLOR_THRESHOLD and error_sum < pre_error_sum:
        if error_sum < constants.TOTAL_COLOR_THRESHOLD and error_sum < pre_error_sum:
            user_id = person_num
            user_bbox_left_top = point_left_top
            user_bbox_right_low = point_right_low
            pre_error_sum = error_sum
            pre_colors = sorted_colors

        # plt.figure()
        # plt.axis("off")
        # plt.imshow(bar)
        # plt.show()

    print("User:", user_id)

    # 사용자 컬러 정보 가중치 부여 저장 부분(확인필요)
    # if user_id != -1:
    #     for idx in range(CLUSTER_NUM):
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

        # plt.figure()
        # plt.axis("off")
        # plt.imshow(cropped_image_original)
        # plt.show()
    else:
        print("************* WARNING: Couldn't find user!! *************")
        state_no_user = True


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print('server start')
    num_connected = 0

    tracker = re3_tracker.Re3Tracker()

    while True:
        client_socket, addr = server_socket.accept()
        recv_packet = client_socket.recv(1024).decode()
        print(recv_packet)

        if recv_packet == '1;CART':
            pass
            start_new_thread(communication_cart, (client_socket, enclosure_queue,))
            start_new_thread(manual_control_cart, (enclosure_queue,))
            # start_new_thread(test_cart_input, (enclosure_queue,))
        elif recv_packet == '2;AZURE':
            start_new_thread(wait_accept_socket, (server_socket, enclosure_queue,))
            # start_new_thread(test_cart_input, (enclosure_queue,))
            break

    while True:
        # 여기에 AZURE 수신 한 뒤 Re3 부분 추가
        # 거리, 각도 값에 따라 모터 명령 코드를 추가
        # 모터 명령을 enclosure_queue에 put 한다(manual_control_cart 함수 참고)
        # pass

        cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Webcam', OUTPUT_WIDTH, OUTPUT_HEIGHT)

        while True:
            start = time.time()

            # 이미지 데이터 받아오기
            stringData = recvall(client_socket, 691200)

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

            # bytes 형태의 point list 정보를 list로 변환
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
            angle_list = ''
            if angle_data_len > 0:
                angle_list = list(ast.literal_eval(stringAngleData.decode('utf-8')))
            print("angle_list: ", angle_list)

            # bytes 형태의 distance list 정보를 list로 변환
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
                if frameNum % constants.CHECK_USER_FRAME_NUM == 0:
                    check_user(decimg, candidate_num, point_list)
                    isVerified = True
                else:
                    track_in_image(decimg)
                    isVerified = False
            else:
                if frameNum % constants.FIND_USER_FRAME_NUM == 0:
                    check_user(decimg, candidate_num, point_list)
                    isVerified = True
                else:
                    isVerified = False

            # 유저가 존재하고, verifier가 동작한 후라면 유저 정보가 있으므로 모터 조정 가능
            if (not state_no_user) and isVerified:
                # 키넥트 기준 계산한 각도와 거리 정보
                difference_angle = angle_list[user_id] - 90
                user_distance = distance_list[user_id]
                # 유저와의 거리가 100이하라면
                if user_distance < constants.LIMIT_DISTANCE:
                    # 멈춤(거리유지 위해)
                    # pass
                    wheel1_speed = 0
                    wheel2_speed = 0
                    wheel3_speed = 0
                    wheel4_speed = 0
                    motor_control = 'S,' + str(wheel1_speed) + ';S,' + str(wheel2_speed) \
                                    + ";S," + str(wheel3_speed) + ";S," + str(wheel4_speed) + ";G"
                    enclosure_queue.put(motor_control)
                    print("Raspberry: ", motor_control, "//time:", datetime.now())
                # 각도가 -10 이하라면
                elif difference_angle < -constants.LIMIT_STRAIGHT:
                    # 우회전(각도별로 나눠야)
                    # enclosure_queue.put('F,100;F,100;F,40;F,100;N')

                    if difference_angle < -constants.LIMIT_TURN_4:
                        wheel1_speed = constants.WHEEL1_R4_SPEED
                        wheel2_speed = constants.WHEEL2_R4_SPEED
                        wheel3_speed = constants.WHEEL3_R4_SPEED
                        wheel4_speed = constants.WHEEL4_R4_SPEED
                        motor_control = 'F,' + str(wheel1_speed) + ';B,' + str(wheel2_speed) \
                                        + ";F," + str(wheel3_speed) + ";B," + str(wheel4_speed) + ";N"

                        print("Raspberry: ", motor_control, "//time:", datetime.now())
                        enclosure_queue.put(motor_control)

                    elif difference_angle < -constants.LIMIT_TURN_3:
                        wheel1_speed = constants.WHEEL1_R3_SPEED
                        wheel2_speed = constants.WHEEL2_R3_SPEED
                        wheel3_speed = constants.WHEEL3_R3_SPEED
                        wheel4_speed = constants.WHEEL4_R3_SPEED
                        motor_control = 'F,' + str(wheel1_speed) + ';F,' + str(wheel2_speed) \
                                        + ";F," + str(wheel3_speed) + ";F," + str(wheel4_speed) + ";N"

                        print("Raspberry: ", motor_control, "//time:", datetime.now())
                        enclosure_queue.put(motor_control)

                    elif difference_angle < -constants.LIMIT_TURN_2:
                        wheel1_speed = constants.WHEEL1_R2_SPEED
                        wheel2_speed = constants.WHEEL2_R2_SPEED
                        wheel3_speed = constants.WHEEL3_R2_SPEED
                        wheel4_speed = constants.WHEEL4_R2_SPEED
                        motor_control = 'F,' + str(wheel1_speed) + ';F,' + str(wheel2_speed)\
                                        + ";F," + str(wheel3_speed) + ";F," + str(wheel4_speed) + ";N"

                        print("Raspberry: ", motor_control, "//time:", datetime.now())
                        enclosure_queue.put(motor_control)

                    else:
                        wheel1_speed = constants.WHEEL1_R1_SPEED
                        wheel2_speed = constants.WHEEL2_R1_SPEED
                        wheel3_speed = constants.WHEEL3_R1_SPEED
                        wheel4_speed = constants.WHEEL4_R1_SPEED
                        motor_control = 'F,' + str(wheel1_speed) + ';F,' + str(wheel2_speed) \
                                        + ";F," + str(wheel3_speed) + ";F," + str(wheel4_speed) + ";N"

                        print("Raspberry: ", motor_control, "//time:", datetime.now())
                        enclosure_queue.put(motor_control)

                # 각도가 10도 이상이라면
                elif difference_angle > constants.LIMIT_STRAIGHT:
                    # 좌회전(각도별로 나눠야)
                    # enclosure_queue.put('F,100;F,100;F,100;F,40;N')

                    if difference_angle > constants.LIMIT_TURN_3:
                        wheel1_speed = constants.WHEEL1_L4_SPEED
                        wheel2_speed = constants.WHEEL2_L4_SPEED
                        wheel3_speed = constants.WHEEL3_L4_SPEED
                        wheel4_speed = constants.WHEEL4_L4_SPEED
                        motor_control = 'B,' + str(wheel1_speed) + ';F,' + str(wheel2_speed) \
                                        + ";B," + str(wheel3_speed) + ";F," + str(wheel4_speed) + ";N"

                        print("Raspberry: ", motor_control, "//time:", datetime.now())
                        enclosure_queue.put(motor_control)

                    # elif difference_angle > constants.LIMIT_TURN_2:
                    #     wheel1_speed = constants.WHEEL1_L2_SPEED
                    #     wheel2_speed = constants.WHEEL2_L2_SPEED
                    #     wheel3_speed = constants.WHEEL3_L2_SPEED
                    #     wheel4_speed = constants.WHEEL4_L2_SPEED
                    #     motor_control = 'F,' + str(wheel1_speed) + ';F,' + str(wheel2_speed) \
                    #                     + ";F," + str(wheel3_speed) + ";F," + str(wheel4_speed) + ";N"
                    #
                    #     print("Raspberry: ", motor_control, "//time:", datetime.now())
                    #     enclosure_queue.put(motor_control)

                    else:
                        wheel1_speed = constants.WHEEL1_L3_SPEED
                        wheel2_speed = constants.WHEEL2_L3_SPEED
                        wheel3_speed = constants.WHEEL3_L3_SPEED
                        wheel4_speed = constants.WHEEL4_L3_SPEED
                        motor_control = 'F,' + str(wheel1_speed) + ';F,' + str(wheel2_speed) \
                                        + ";F," + str(wheel3_speed) + ";F," + str(wheel4_speed) + ";N"

                        print("Raspberry: ", motor_control, "//time:", datetime.now())
                        enclosure_queue.put(motor_control)
                    #     wheel1_speed = constants.WHEEL1_L1_SPEED
                    #     wheel2_speed = constants.WHEEL2_L1_SPEED
                    #     wheel3_speed = constants.WHEEL3_L1_SPEED
                    #     wheel4_speed = constants.WHEEL4_L1_SPEED
                    #     motor_control = 'F,' + str(wheel1_speed) + ';F,' + str(wheel2_speed) \
                    #                     + ";F," + str(wheel3_speed) + ";F," + str(wheel4_speed) + ";N"
                    #
                    #     print("Raspberry: ", motor_control, "//time:", datetime.now())
                    #     enclosure_queue.put(motor_control)

                # 그 외 상황에 대해서는 직진
                else:
                    # 직진
                    # pass
                    wheel1_speed = constants.WHEEL1_F_SPEED
                    wheel2_speed = constants.WHEEL2_F_SPEED
                    wheel3_speed = constants.WHEEL3_F_SPEED
                    wheel4_speed = constants.WHEEL4_F_SPEED
                    motor_control = 'F,' + str(wheel1_speed) + ';F,' + str(wheel2_speed) \
                                    + ";F," + str(wheel3_speed) + ";F," + str(wheel4_speed) + ";N"

                    print("Raspberry: ", motor_control, "//time:", datetime.now())
                    enclosure_queue.put(motor_control)

                not_found_count = 0
            # 만일 유저를 찾지 못했다면(간섭)
            elif state_no_user and len(user_hsv_values) != 0 and isVerified:
                # 3 번 확인, 두번째 간섭 시 감속, 네번째 멈춤(간섭상황)
                if not_found_count == 19:
                    wheel1_speed = 0
                    wheel2_speed = 0
                    wheel3_speed = 0
                    wheel4_speed = 0
                    motor_control = 'S,' + str(wheel1_speed) + ';S,' + str(wheel2_speed) \
                                    + ";S," + str(wheel3_speed) + ";S," + str(wheel4_speed) + ";B"
                    enclosure_queue.put(motor_control)

                    print("Raspberry: ", motor_control, "//time:", datetime.now())
                    enclosure_queue.put(motor_control)
                elif not_found_count == 9:
                    wheel1_speed = int(wheel1_speed * 0.7)
                    wheel2_speed = int(wheel2_speed * 0.7)
                    wheel3_speed = int(wheel3_speed * 0.7)
                    wheel4_speed = int(wheel4_speed * 0.7)
                    motor_control = 'F,' + str(wheel1_speed) + ';F,' + str(wheel2_speed) \
                                    + ";F," + str(wheel3_speed) + ";F," + str(wheel4_speed) + ";N"

                    print("Raspberry: ", motor_control, "//time:", datetime.now())
                    enclosure_queue.put(motor_control)

                not_found_count += 1

            cv2.imshow('Webcam', decimg)

            key = cv2.waitKey(1)
            if key == 27:
                break

            frameNum += 1

            print("[", frameNum, "], time:", time.time() - start, "===========================")

