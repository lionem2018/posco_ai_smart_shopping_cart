#include "kinect.hpp"
#include "util.h"

#include <chrono>
#include <math.h>
#include <iostream>
#include <stdio.h>
#include <vector>
#include <fstream>
#include <iterator>
#include <string>
#include <time.h>
//#include <WinSock2.h>

# define	FILE_PATH		"C:/Users/PIRL/source/repos/AzureKinect/AzureKinect"
# define	MIN_BOX_WIDTH	80
# define	VALID_RANGE		25

/*------ Base64 Encoding Table ------*/
static const char MimeBase64[] = {
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
	'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
	'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
	'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
	'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
	'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
	'w', 'x', 'y', 'z', '0', '1', '2', '3',
	'4', '5', '6', '7', '8', '9', '+', '/'
};


using namespace std;

// Constructor
kinect::kinect(const uint32_t index)
	: device_index(index)
{
	// Initialize
	initialize();
}

kinect::~kinect()
{
	// Finalize
	finalize();
}

// Initialize
void kinect::initialize()
{
	// Initialize Sensor
	initialize_sensor();

	// Initialize Body Tracking
	initialize_body_tracking();

	// 이미지 경로 및 좌표 데이터 저장
	out.open("./bboxes.txt", ios::ate);
}

// Initialize Sensor
inline void kinect::initialize_sensor()
{
	// Get Connected Devices
	const int32_t device_count = k4a::device::get_installed_count();
	if (device_count == 0) {
		throw k4a::error("Failed to found device!");
	}

	// Open Default Device
	device = k4a::device::open(device_index);

	// Start Cameras with Configuration
	device_configuration = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
	device_configuration.color_format = k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_BGRA32;
	device_configuration.color_resolution = k4a_color_resolution_t::K4A_COLOR_RESOLUTION_720P;
	device_configuration.depth_mode = k4a_depth_mode_t::K4A_DEPTH_MODE_NFOV_UNBINNED;
	device_configuration.synchronized_images_only = true;
	device_configuration.wired_sync_mode = k4a_wired_sync_mode_t::K4A_WIRED_SYNC_MODE_STANDALONE;
	device.start_cameras(&device_configuration);

	// Get Calibration
	calibration = device.get_calibration(device_configuration.depth_mode, device_configuration.color_resolution);
}

// Initialize Body Tracking
inline void kinect::initialize_body_tracking()
{
	// Set Tracker Configuration
	k4abt_tracker_configuration_t tracker_configuration = K4ABT_TRACKER_CONFIG_DEFAULT;
	tracker_configuration.sensor_orientation = K4ABT_SENSOR_ORIENTATION_DEFAULT;
	tracker_configuration.cpu_only_mode = false;

	// Create Tracker with Configuration
	tracker = k4abt::tracker::create(calibration, tracker_configuration);
	if (!tracker) {
		throw k4a::error("Failed to create tracker!");
	}

	// Set Temporal Smoothing Filter [0.0-1.0]
	constexpr float smoothing_factor = K4ABT_DEFAULT_TRACKER_SMOOTHING_FACTOR;
	tracker.set_temporal_smoothing(smoothing_factor);

	// Create Color Table
	colors.push_back(cv::Vec3b(255, 0, 0));
	colors.push_back(cv::Vec3b(0, 255, 0));
	colors.push_back(cv::Vec3b(0, 0, 255));
	colors.push_back(cv::Vec3b(255, 255, 0));
	colors.push_back(cv::Vec3b(0, 255, 255));
	colors.push_back(cv::Vec3b(255, 0, 255));
	colors.push_back(cv::Vec3b(128, 0, 0));
	colors.push_back(cv::Vec3b(0, 128, 0));
	colors.push_back(cv::Vec3b(0, 0, 128));
	colors.push_back(cv::Vec3b(128, 128, 0));
	colors.push_back(cv::Vec3b(0, 128, 128));
	colors.push_back(cv::Vec3b(128, 0, 128));
}

// Finalize
void kinect::finalize()
{
	// Destroy Tracker
	tracker.destroy();

	// Stop Cameras
	device.stop_cameras();

	// Close Device
	device.close();

	// Close Window
	cv::destroyAllWindows();

	out.close();
}

// Run
void kinect::run(SOCKET socket)
//void kinect::run()
{
	int pre_people_num = 0;
	int candidate_list[10];
	float user_distance = 0.0;

	frame_num = 0;

	for (int i = 0; i < 10; i++)
	{
		candidate_list[i] = -1;
	}

	// Main Loop
	while (true) {

		// Update
		update(pre_people_num, candidate_list, user_distance);

		// Draw
		draw();

		// Show
		show(candidate_list, socket);
		//show(candidate_list);

		// Wait Key
		constexpr int32_t delay = 1;
		const int32_t key = cv::waitKey(delay);
		if (key == 'q') {
			break;
		}

		frame_num++;
	}
}

// Update
void kinect::update(int& pre_people_num, int * candidate_list, float& user_distance)
{
	// Update Frame
	update_frame();

	// Update Body Tracking
	update_body_tracking();

	// Update Inference
	update_inference();

	// Update Skeleton
	update_skeleton(pre_people_num, candidate_list, user_distance);

	// Release Capture Handle
	capture.reset();

	// Release Body Frame Handle
	frame.reset();
}

// Update Frame
inline void kinect::update_frame()
{
	// Get Capture Frame
	constexpr std::chrono::milliseconds time_out(K4A_WAIT_INFINITE);
	const bool result = device.get_capture(&capture, time_out);
	if (!result) {
		this->~kinect();
	}
}

// Update Body Tracking
inline void kinect::update_body_tracking()
{
	// Enqueue Capture
	tracker.enqueue_capture(capture);

	// Pop Body Tracking Result
	frame = tracker.pop_result();

	start = clock();
}

// Update Inference
void kinect::update_inference()
{
	// Get Image that used for Inference
	k4a::capture capture = frame.get_capture();
	color_image = capture.get_color_image();

	// Release Capture Handle
	capture.reset();
}

// Update Skeleton
inline void kinect::update_skeleton(int& pre_people_num, int* candidate_list, float& user_distance)
{
	float distance_list[10] = { 0 };
	int id_list[10] = { 0 };
	// Clear Bodies
	bodies.clear();

	// Get Bodies
	const int32_t num_bodies = static_cast<int32_t>(frame.get_num_bodies());
	bodies.resize(num_bodies);

	// 거리 각도 계산하는 코드
	for (int32_t i = 0; i < num_bodies; i++) {
		k4abt_skeleton_t skeleton = frame.get_body(i).skeleton;
		k4abt_joint_t joint_pelvis = skeleton.joints[0];
		k4abt_joint_t joint_head = skeleton.joints[26];
		k4abt_joint_t joint_neck = skeleton.joints[3];
		k4abt_joint_t joint_spine_chest = skeleton.joints[2];
		k4abt_joint_t joint_hip_left = skeleton.joints[18];
		k4abt_joint_t joint_hip_right = skeleton.joints[22];
		k4abt_joint_t joint_ankle_left = skeleton.joints[20];
		k4abt_joint_t joint_ankle_right = skeleton.joints[24];
		k4abt_joint_t joint_shoulder_left = skeleton.joints[5];
		k4abt_joint_t joint_shoulder_right = skeleton.joints[12];

		k4a_float3_t point_center;
		point_center.xyz.x = (joint_ankle_left.position.xyz.x + joint_ankle_right.position.xyz.x) / 2;
		point_center.xyz.y = (joint_ankle_left.position.xyz.y + joint_ankle_right.position.xyz.y) / 2;
		point_center.xyz.z = (joint_ankle_left.position.xyz.z + joint_ankle_right.position.xyz.z) / 2;


		float distance_hip = sqrt(pow(joint_hip_left.position.xyz.x - joint_hip_right.position.xyz.x, 2) + pow(joint_hip_left.position.xyz.y - joint_hip_right.position.xyz.y, 2) + pow(joint_hip_left.position.xyz.z - joint_hip_right.position.xyz.z, 2));
		float distance_neck = sqrt(pow(joint_neck.position.xyz.x - joint_spine_chest.position.xyz.x, 2) + pow(joint_neck.position.xyz.y - joint_spine_chest.position.xyz.y, 2) + pow(joint_neck.position.xyz.z - joint_spine_chest.position.xyz.z, 2));
		float distance_center = sqrt(pow(point_center.xyz.z, 2));
		float distance_pelnis = sqrt(pow(joint_pelvis.position.xyz.x, 2) + pow(joint_pelvis.position.xyz.y, 2) + pow(joint_pelvis.position.xyz.z, 2));
		float distance_neck_pelnis = sqrt(pow(joint_neck.position.xyz.x - joint_pelvis.position.xyz.x, 2) + pow(joint_neck.position.xyz.y - joint_pelvis.position.xyz.y, 2) + pow(joint_neck.position.xyz.z - joint_pelvis.position.xyz.z, 2));
		float distance_head_ankle = sqrt(pow(joint_head.position.xyz.x - joint_ankle_right.position.xyz.x, 2) + pow(joint_head.position.xyz.y - joint_ankle_right.position.xyz.y, 2) + pow(joint_head.position.xyz.z - joint_ankle_right.position.xyz.z, 2));
		float distance_shoulder = sqrt(pow(joint_shoulder_left.position.xyz.x - joint_shoulder_right.position.xyz.x, 2) + pow(joint_shoulder_left.position.xyz.y - joint_shoulder_right.position.xyz.y, 2) + pow(joint_shoulder_left.position.xyz.z - joint_shoulder_right.position.xyz.z, 2));


		float distance_rate = distance_hip * distance_center;

		printf_s("id %d: xyz(%f, %f, %f) / distance_rate = %f / distance_hip = %f / distance_z = %f\n", frame.get_body(i).id, skeleton.joints[0].position.xyz.x, skeleton.joints[0].position.xyz.y, skeleton.joints[0].position.xyz.z, distance_rate, distance_neck_pelnis, distance_center);
		printf_s("angle: %d\n", (int)(atan2(joint_pelvis.position.xyz.z, joint_pelvis.position.xyz.x) / 3.141592 * 180));
		bodies.emplace_back(frame.get_body(i));

		distance_list[i] = distance_neck_pelnis;
		id_list[i] = frame.get_body(i).id;
	}

	// 등록된 유저 정보가 없음 => 0번째 사람이 유저로 인식
	if (user_distance == 0 && distance_list[0] != 0.0)
	{
		user_distance = distance_list[0];
		printf_s("save user information: %f\n", distance_list[0]);
	}
	
	// 이전 프레임과 비교하여 사람 수가 변했다면 유저 후보 추적
	if (pre_people_num != num_bodies)
	{
		printf_s("change people number!\n");
		pre_people_num = num_bodies;
	}

	get_candidate_list(num_bodies, user_distance, distance_list, id_list, candidate_list);
}

void kinect::get_candidate_list(const int num_bodies, const float user_distance, float * distance_list, int* id_list, int* candidate_list)
{
	for (int32_t i = 0; i < 10; i++)
	{
		candidate_list[i] = -1;
	}

	int count = 0;
	for (int32_t i = 0; i < num_bodies; i++)
	{
		if (distance_list[i] > user_distance - VALID_RANGE && distance_list[i] < user_distance + VALID_RANGE)
		{
			candidate_list[count] = id_list[i];
			count++;
		}
	}
}

// Draw
void kinect::draw()
{
	// Draw Color
	draw_color();
}

// Draw Color
inline void kinect::draw_color()
{
	if (!color_image.handle()) {
		return;
	}

	// Get cv::Mat from k4a::image
	color = k4a::get_mat(color_image);

	// Release Skeleton Image Handle
	color_image.reset();
}

// Show
void kinect::show(int* candidate_list, SOCKET socket)
//void kinect::show(int * candidate_list)
{
	// Show Skeleton
	//show_skeleton(candidate_list);
	show_skeleton(candidate_list, socket);
}

// Show Skeleton
//inline void kinect::show_skeleton(int* candidate_list)
inline void kinect::show_skeleton(int * candidate_list, SOCKET socket)
{

	string pointsStringData("");
	string anglesStringData("");
	int candidate_num = 0;

	// Visualize Skeleton
	for (const k4abt_body_t& body: bodies) {
		//int32_t id = candidate_list[i];
		// const k4abt_body_t& body = bodies[id];

		k4abt_joint_t joint_neck = body.skeleton.joints[3];
		k4a_float2_t position_neck;
		const bool result_neck = calibration.convert_3d_to_2d(joint_neck.position, k4a_calibration_type_t::K4A_CALIBRATION_TYPE_DEPTH, k4a_calibration_type_t::K4A_CALIBRATION_TYPE_COLOR, &position_neck);

		k4abt_joint_t joint_pelvis = body.skeleton.joints[0];
		k4a_float2_t position_pelvis;
		const bool result_pelvis = calibration.convert_3d_to_2d(joint_pelvis.position, k4a_calibration_type_t::K4A_CALIBRATION_TYPE_DEPTH, k4a_calibration_type_t::K4A_CALIBRATION_TYPE_COLOR, &position_pelvis);
		
		k4abt_joint_t joint_shoulder_right = body.skeleton.joints[12];
		k4a_float2_t position_shoulder_right;
		const bool result_shoulder_right = calibration.convert_3d_to_2d(joint_shoulder_right.position, k4a_calibration_type_t::K4A_CALIBRATION_TYPE_DEPTH, k4a_calibration_type_t::K4A_CALIBRATION_TYPE_COLOR, &position_shoulder_right);

		k4abt_joint_t joint_shoulder_left = body.skeleton.joints[5];
		k4a_float2_t position_shoulder_left;
		const bool result_shoulder_left = calibration.convert_3d_to_2d(joint_shoulder_left.position, k4a_calibration_type_t::K4A_CALIBRATION_TYPE_DEPTH, k4a_calibration_type_t::K4A_CALIBRATION_TYPE_COLOR, &position_shoulder_left);


		k4abt_joint_t joint_knee_left = body.skeleton.joints[19];
		k4a_float2_t position_knee_left;
		const bool result_knee_left = calibration.convert_3d_to_2d(joint_knee_left.position, k4a_calibration_type_t::K4A_CALIBRATION_TYPE_DEPTH, k4a_calibration_type_t::K4A_CALIBRATION_TYPE_COLOR, &position_knee_left);

		k4abt_joint_t joint_knee_right = body.skeleton.joints[23];
		k4a_float2_t position_knee_right;
		const bool result_knee_right = calibration.convert_3d_to_2d(joint_knee_right.position, k4a_calibration_type_t::K4A_CALIBRATION_TYPE_DEPTH, k4a_calibration_type_t::K4A_CALIBRATION_TYPE_COLOR, &position_knee_right);


		//float distance = sqrt(pow());
		int width = sqrt(pow(position_shoulder_right.xy.x - position_shoulder_left.xy.x, 2));

		if (width < MIN_BOX_WIDTH)
			width = MIN_BOX_WIDTH;

		const cv::Point point_rect_left_top(static_cast<int>(position_neck.xy.x - width/2), static_cast<int>(position_neck.xy.y));
		const cv::Point point_rect_right_low(static_cast<int>(position_neck.xy.x + width/2), static_cast<int>(position_knee_left.xy.y));
		
		/*
		if (position_shoulder_right.xy.x > position_shoulder_left.xy.x)
		{
			const cv::Point point_rect_left_top(static_cast<int>(position_shoulder_left.xy.x), static_cast<int>(position_shoulder_left.xy.y));
			const cv::Point point_rect_right_low(static_cast<int>(position_shoulder_left.xy.x + width), static_cast<int>(position_knee_right.xy.y));
		}
		*/

		// 해당 사람이 유저 후보군일 경우 어깨부터 무릎까지의 경계박스를 위한 좌표 저장
		if (isCandidate(candidate_list, body.id))
		{
			if (candidate_num > 0)
			{
				pointsStringData += ",";
				anglesStringData += ",";
			}

			// bounding box 위치 string 형태로 저장
			pointsStringData += "[" + to_string(point_rect_left_top.x / 2) + "," + to_string(point_rect_left_top.y / 2) + "]" + "," + "[" + to_string(point_rect_right_low.x / 2) + "," + to_string(point_rect_right_low.y / 2) + "]";
			//pointsStringData += "[" + to_string(point_rect_left_top.x / 1280 * 120) + "," + to_string(point_rect_left_top.y / 720 * 260) + "]" + "," + "[" + to_string(point_rect_right_low.x / 1280 * 120) + "," + to_string(point_rect_right_low.y / 720 * 260) + "]";

			// 카메라 중심으로 각도 계산 및 string 형태로 저장
			int angle = (int)(atan2(joint_pelvis.position.xyz.z, joint_pelvis.position.xyz.x) / 3.141592 * 180);
			anglesStringData += "[" + to_string(angle) + "]";

			// 경계박스 이미지에 그리기
			//cv::rectangle(color, point_rect_left_top, point_rect_right_low, colors[(body.id - 1) % colors.size()]);

			candidate_num++;
		}
		// isCandidate(candidate_list, body.id);

		// 골격 조인트 이미지에 출력
		/*
		for (const k4abt_joint_t& joint : body.skeleton.joints) {
			k4a_float2_t position;
			const bool result = calibration.convert_3d_to_2d(joint.position, k4a_calibration_type_t::K4A_CALIBRATION_TYPE_DEPTH, k4a_calibration_type_t::K4A_CALIBRATION_TYPE_COLOR, &position);
			if (!result) {
				continue;
			}

			const int32_t thickness = (joint.confidence_level >= k4abt_joint_confidence_level_t::K4ABT_JOINT_CONFIDENCE_MEDIUM) ? -1 : 1;
			const cv::Point point(static_cast<int32_t>(position.xy.x), static_cast<int32_t>(position.xy.y));
			cv::circle(color, point, 5, colors[(body.id - 1) % colors.size()], thickness);
		}
		*/
	}
	cv::Mat resized_color;
	cv::cvtColor(color, resized_color, cv::COLOR_BGRA2BGR);
	cv:resize(resized_color, resized_color, cv::Size(640, 360), 0, 0, cv::INTER_LINEAR);
	//cv:resize(resized_color, resized_color, cv::Size(260, 120), 0, 0, cv::INTER_LINEAR);

	// 프레임 저장 or 전송
	//char file_name[1024];
	/*if (frame_num % 3 == 0)
	{*/
		// 이미지 파일로 저장
		//sprintf_s(file_name, "%s/images/kinect_%d.png", FILE_PATH, frame_num);
		//printf_s("%s\n", file_name);
		//cv::imwrite(file_name, color);

		////cout << color << endl;

		//cout << pointsStringData << endl;

		//// 해당 프레임 내의 후보자 수, 각 후보당 bonding box의 좌측 상단과 우측 하단 좌표 저장
		out << candidate_num << ";" << "[" << pointsStringData << "]" << endl;

		//printf_s("candidate_num: %d\n", candidate_num);

		////////////////////////////////////////////////////////////
		// 서버 전송 코드 여기에 넣으면 됨

		//const int height = 720;
		//const int width = 1280;
		/*const int height = 360;
		const int width = 640;
		const int channel = 3;

		char buffer[height * width * channel];*/

		/*uchar* p;
		int i, j;
		for (i = 0; i < height; ++i) {
			p = color.ptr<uchar>(i);
			for (j = 0; j < width; ++j) {
				buffer[i * width + j] = p[j];
				
			}
		}*/

		/*for (int y = 0; y < height; y++)
		{
			uchar* pointer = resized_color.ptr<uchar>(y);
			 
			for (int x = 0; x < width; x++)
			{
				uchar b = pointer[x * 3 + 0];
				uchar g = pointer[x * 3 + 1];
				uchar r = pointer[x * 3 + 2];

				buffer[y * width + x * 3 + 0] = b;
				buffer[y * width + x * 3 + 1] = g;
				buffer[y * width + x * 3 + 2] = r;
			}
		}*/

		cout << "[" << frame_num  << "]:::" << resized_color.type() << ":::" << resized_color.cols << ":::" << resized_color.rows << endl;
		//cout << resized_color << endl;

		
		try {
			//send(socket, "921600          ", 16, 0);
			//send(socket, buffer, 921600, 0);

			//send(socket, "2764800          ", 16, 0);
			//send(socket, buffer, 2764800, 0);
			
			//send(socket, "691200          ", 16, 0);
			send(socket, (char*)resized_color.data, 691200, 0);
			//send(socket, (char*)resized_color.data, 93600, 0);

			char char_candidate_num[5] = { 0 };
			char char_candidate_point_data_len[5] = { 0 };
			char char_candidate_angle_data_len[5] = { 0 };
			char* char_candidate_point_data = &pointsStringData[0];
			char* char_candidate_angle_data = &anglesStringData[0];

			sprintf_s(char_candidate_num, "%d", candidate_num);
			for (int i = strlen(char_candidate_num); i < 5; i++)
				char_candidate_num[i] = ' ';
			cout << "point data: " << char_candidate_point_data << endl;

			sprintf_s(char_candidate_point_data_len, "%d", pointsStringData.length());
			for (int i = strlen(char_candidate_point_data_len); i < 5; i++)
				char_candidate_point_data_len[i] = ' ';

			sprintf_s(char_candidate_angle_data_len, "%d", anglesStringData.length());
			for (int i = strlen(char_candidate_angle_data_len); i < 5; i++)
				char_candidate_angle_data_len[i] = ' ';

			send(socket, char_candidate_num, 5, 0);
			send(socket, char_candidate_point_data_len, 5, 0);
			send(socket, char_candidate_point_data, pointsStringData.length(), 0);
			send(socket, char_candidate_angle_data_len, 5, 0);
			send(socket, char_candidate_angle_data, anglesStringData.length(), 0);

			end = clock();

			printf_s("time: %f\n", (double)end - start);
		}
		catch (exception){
			closesocket(socket);
		}
	
		////////////////////////////////////////////////////////////
	//}

	// Show Image
	//const cv::String window_name = cv::format("skeleton (kinect %d)", device_index);
	//cv::imshow(window_name, resized_color);
}

bool kinect::isCandidate(int* candidate_list, int body_id)
{
	for (int i = 0; candidate_list[i] != -1; i++)
	{
		printf_s("%d====%d\n", body_id, candidate_list[i]);
		if (body_id == candidate_list[i])
			return true;
	}

	return false;
}