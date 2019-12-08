# USAGE
# python color_kmeans.py --image images/jp.png --clusters 3

# import the necessary packages
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import argparse
import color_utils
import cv2
import os, ast, copy

user_hsv_values = []
cluster_num = 4
threshold = 150

# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="Path to the image")
# ap.add_argument("-c", "--clusters", required=True, type=int, help="# of clusters")
# args = vars(ap.parse_args())

# load the image and convert it from BGR to RGB so that
# we can dispaly it with matplotlib
# image = cv2.imread(args["image"])

# image = cv2.imread("../images/kinect_1020.png")
# image = image[128:622, 555:709]
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

image_dir = "C:/Users/PIRL/source/repos/AzureKinect/AzureKinect/images"
txt_file_path = "C:/Users/PIRL/source/repos/AzureKinect/AzureKinect/bboxes.txt"

if os.path.exists(image_dir):
    if os.path.isfile(txt_file_path):
        print("Image directory and txt file are okay!!")

with open(txt_file_path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        split_data = line.replace('\n', '').split(";")
        print(split_data)
        file_path = split_data[0]
        candidate_num = int(split_data[1])
        raw_point_list = split_data[2]

        image = cv2.imread(file_path)
        point_list = ast.literal_eval(raw_point_list)

        print(image)

        user_id = -1
        pre_error_sum = 560
        pre_colors = user_hsv_values
        for person_num in range(candidate_num):
            point_left_top = point_list[2*person_num]
            point_right_low = point_list[2*person_num+1]
            print(point_left_top, point_right_low)
            cropped_image = image[point_left_top[1]:point_right_low[1], point_left_top[0]:point_right_low[0]]
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

            print(hist)
            print(sorted_hist)
            # color = clt.cluster_centers_.astype('uint8')
            # color = np.array(clt.cluster_centers_, dtype=np.uint8)

            # colors 추출하여 hist의 값이 큰 순서로 colors 순서 바꾸기
            colors = clt.cluster_centers_.astype('uint8')
            sorted_colors = [colors[i] for i in sorted_idx]
            print(colors)
            print(sorted_colors)

            error_sum = 0
            # convert rgb color value to hsv
            for color_index, color in enumerate(sorted_colors):
                h_error = s_error = v_error = 0
                color = color_utils.rgb_to_hsv(color[0], color[1], color[2])
                print(color_index, ":", color)

                # 유저 컬러 등록
                if len(user_hsv_values) < cluster_num:
                    user_hsv_values.append(color)
                    continue

                if user_hsv_values[color_index][0] > color[0]:
                    if abs(user_hsv_values[color_index][0] - color[0]) < (360 - user_hsv_values[color_index][0] + color[0]):
                        h_error = user_hsv_values[color_index][0] - color[0]
                        print("h error:", abs(user_hsv_values[color_index][0] - color[0]))
                    else:
                        h_error = 360 - user_hsv_values[color_index][0] + color[0]
                        print("h error:", 360 - user_hsv_values[color_index][0] + color[0])
                else:
                    if abs(user_hsv_values[color_index][0] - color[0]) < (360 - color[0] + user_hsv_values[color_index][0]):
                        h_error = user_hsv_values[color_index][0] - color[0]
                        print("h error:", abs(user_hsv_values[color_index][0] - color[0]))
                    else:
                        h_error = 360 - color[0] + user_hsv_values[color_index][0]
                        print("h error:", 360 - color[0] + user_hsv_values[color_index][0])

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
                print(color_range)

            print("error_sum:", error_sum)

            if error_sum < threshold and error_sum < pre_error_sum:
                user_id = person_num
                pre_error_sum = error_sum
                pre_colors = sorted_colors

            # show our color bart
            plt.figure()
            plt.axis("off")
            plt.imshow(bar)
            plt.show()

        print("User:", user_id)
        for idx in range(cluster_num):
            user_hsv_values[idx][0] = user_hsv_values[idx][0] * 0.8 + pre_colors[idx][0] * 0.2
            user_hsv_values[idx][1] = user_hsv_values[idx][1] * 0.8 + pre_colors[idx][1] * 0.2
            user_hsv_values[idx][2] = user_hsv_values[idx][2] * 0.8 + pre_colors[idx][2] * 0.2
        print(user_hsv_values)

