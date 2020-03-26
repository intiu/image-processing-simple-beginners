#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/video/background_segm.hpp>
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <iostream>
#include <string>


using namespace cv;
using namespace std;


Mat gray, cimg, img, edges;

int initThresh;
const int maxThresh = 200;
double p1, p2;

vector<Vec3f> circles;

void onTrackbarChange(int, void*) {
	cimg = img.clone();

	p1 = initThresh;
	p2 = initThresh * 0.4;

	HoughCircles(gray, circles, HOUGH_GRADIENT, 1, cimg.rows / 64, p1, p2, 25, 50);

	for (size_t i = 0; i < circles.size(); i++)
	{
		Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
		int radius = cvRound(circles[i][2]);
		circle(cimg, center, radius, Scalar(0, 255, 0), 2);
		circle(cimg, center, 2, Scalar(0, 0, 255), 3);
	}

	imshow("Image", cimg);

	Canny(gray, edges, p1, p2);
	imshow("Edges", edges);
}


int main(int argc, char** argv) {
	const char* file = argv[1];
	img = imread("brown-eyes.jpg", IMREAD_COLOR);

	if (img.empty())
	{
		cout << "Error reading image" << file << endl;
		return -1;
	}

	cvtColor(img, gray, COLOR_BGR2GRAY);

	namedWindow("Edges", 1);
	namedWindow("Image", 1);

	initThresh = 105;

	createTrackbar("Threshold", "Image", &initThresh, maxThresh, onTrackbarChange);
	onTrackbarChange(initThresh, 0);

	imshow("Image", img);
	while (true)
	{
		int key;
		key = waitKey(0);
		if ((char)key == 27)
		{
			break;
		}
	}

	destroyAllWindows();

}
