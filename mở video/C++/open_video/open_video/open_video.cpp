﻿#include <opencv2/opencv.hpp>
#include <iostream>

using namespace std;
using namespace cv;

int main() {

	VideoCapture cap("road_car_view.mp4");
	if (!cap.isOpened()) {
		cout << "Error opening video stream or file" << endl;
		return -1;
	}

	while (1) {

		Mat frame;
		cap >> frame;
		if (frame.empty())
			break;
		imshow("Video", frame);
		char c = (char)waitKey(25);
		if (c == 27)
			break;
	}
	cap.release();
	destroyAllWindows();
	return 0;
}