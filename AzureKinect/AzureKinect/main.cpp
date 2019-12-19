#include "kinect.hpp"

#include <iostream>
#include <sstream>

#include <WinSock2.h>


struct socketStruct {
	int nrData;
	double data[100];
};


#define PORT		8888
//#define SERVER_IP	"127.0.0.1"
#define SERVER_IP	"141.223.140.54"

void ErrorHandling(char* message);


int main(int argc, char* argv[])
{
	SOCKET hSocket;

	char ID[] = "2;AZURE";

	WSADATA wsaData;
	hSocket = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);

	SOCKADDR_IN tAddr;
	tAddr.sin_family = AF_INET;
	tAddr.sin_port = htons(PORT);
	tAddr.sin_addr.s_addr = inet_addr(SERVER_IP);

	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
		printf("error1");

	hSocket = socket(PF_INET, SOCK_STREAM, 0);

	if (hSocket == INVALID_SOCKET)
		printf("error2");

	try { 
		if (connect(hSocket, (SOCKADDR*)&tAddr, sizeof(tAddr)) == SOCKET_ERROR)
			printf("error3");

		send(hSocket, ID, strlen(ID), 0);
		/*char dummy_buff[16];
		recv(hSocket, dummy_buff, 16, 0);
		printf(dummy_buff, 3);*/
	}
	catch (const k4a::error & error) {
		
	}

	try {
		kinect kinect;
		kinect.run(hSocket);
		//kinect.run();
	}
	catch (const k4a::error & error) {
		std::cout << error.what() << std::endl;
	}

	return 0;
}

