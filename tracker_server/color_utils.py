# import the necessary packages
import numpy as np
import cv2

color_range_end = [20, 51, 60, 80, 138, 168, 200, 245, 275, 315, 350]
sv_group_num = 4

def centroid_histogram(clt):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)

	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()

	# return the histogram
	return hist

def plot_colors(hist, centroids):
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0

	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		endX = startX + (percent * 300)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
			color.astype("uint8").tolist(), -1)
		startX = endX
	
	# return the bar chart
	return bar


def rgb_to_hsv(r, g, b):
	r, g, b = r/255.0, g/255.0, b/255.0
	mx = max(r, g, b)
	mn = min(r, g, b)
	df = mx-mn
	if mx == mn:
		h = 0
	elif mx == r:
		h = (60 * ((g-b)/df) + 360) % 360
	elif mx == g:
		h = (60 * ((b-r)/df) + 120) % 360
	elif mx == b:
		h = (60 * ((r-g)/df) + 240) % 360
	if mx == 0:
		s = 0
	else:
		s = (df/mx)*100
	v = mx*100

	return list((h, s, v))


def hsv_to_color_range(h, s, v):
	h_range = h
	if (h <= color_range_end[0]) or (h > color_range_end[10]):
		h_range = 0
	else:
		for i in range(1, 11):
			if h <= color_range_end[i]:
				h_range = i
				break

	s_range = s // 25
	if s_range == 4:
		s_range = s_range - 1

	v_range = v // 25
	if v_range == 4:
		v_range = v_range - 1

	return h_range, s_range.astype('uint8'), v_range.astype('uint8')
