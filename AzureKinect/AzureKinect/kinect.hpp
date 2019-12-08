#ifndef __KINECT__
#define __KINECT__

#include <k4a/k4a.hpp>
#include <k4abt.hpp>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <fstream>
#include <vector>
#include <WinSock2.h>
#include <time.h>


class kinect
{
private:
	// Kinect
	k4a::device device;
	k4a::capture capture;
	k4a::calibration calibration;
	k4a_device_configuration_t device_configuration;
	uint32_t device_index;

	// Color
	k4a::image color_image;
	cv::Mat color;

	// Body Tracking
	k4abt::tracker tracker;
	k4abt::frame frame;

	// Skeleton
	std::vector<k4abt_body_t> bodies;

	// Visualize
	std::vector<cv::Vec3b> colors;

	// frame 숫자
	int32_t frame_num;

	// 파일 저장용(임시)
	std::ofstream out;

	clock_t start, end;

public:
	// Constructor
	kinect(const uint32_t index = K4A_DEVICE_DEFAULT);

	// Destructor
	~kinect();

	// Run
	void run(SOCKET);
	//void run();

	// Update
	void update(int&, int *, float&);

	// Draw
	void draw();

	// Show
	//void show(int*);
	void show(int*, SOCKET);

private:
	// Initialize
	void initialize();

	// Initialize Sensor
	void initialize_sensor();

	// Initialize Body Tracking
	void initialize_body_tracking();

	// Finalize
	void finalize();

	// Update Frame
	void update_frame();

	// Update Body Tracking
	void update_body_tracking();

	// Update Inference
	void update_inference();

	// Update Skeleton
	void update_skeleton(int&, int*, float&);

	// Draw Color
	void draw_color();

	// Show Skeleton
	//void show_skeleton(int*);
	void show_skeleton(int *, SOCKET);

	// 유저 후보 리스트 갱신
	void get_candidate_list(const int, const float, float *, int*, int *);

	// 해당 아이디가 유저 후보인지 확인
	bool isCandidate(int*, const int);

	// cv::Mat 이미지 저장
	void save_image();
};

#endif // __KINECT__#pragma once
