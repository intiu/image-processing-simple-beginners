#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <iostream>

using namespace cv;
using namespace std;

Mat dst, cimg, gray, img, edges;

int initThresh;
const int maxThresh = 1000;
double th1, th2;

vector<Vec4i> lines;

void onTrackbarChange(int, void*)
{
	cimg = img.clone();
	dst = img.clone();

	th1 = initThresh;
	th2 = th1 * 0.4;

	Canny(img, edges, th1, th2);

	HoughLinesP(edges, lines, 2, CV_PI / 180, 50, 10, 100);

	for (size_t i = 0; i < lines.size(); i++)
	{
		Vec4i l = lines[i];
		line(dst, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0, 0, 255), 1, LINE_AA);
	}

	imshow("Result Image", dst);
	imshow("Edges", edges);
}

int main(int argc, char** argv) {
	const char* file = argv[1];
	img = imread("lanes.jpg", 1);
	dst = img.clone();

	if (img.empty())
	{
		cout << "Error in reading image" << file << endl;
		return -1;
	}

	cvtColor(img, gray, COLOR_BGR2GRAY);

	namedWindow("Edges", 1);
	namedWindow("Result Image", 1);

	initThresh = 500;

	createTrackbar("threshold", "Result Image", &initThresh, maxThresh, onTrackbarChange);
	onTrackbarChange(initThresh, 0);

	while (true)
	{
		int key;
		key = waitKey(1);
		if ((char)key == 27)
		{
			break;
		}
	}

	destroyAllWindows();
}
