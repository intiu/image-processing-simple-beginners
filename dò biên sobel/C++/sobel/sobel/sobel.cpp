#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "iostream"

using namespace cv;
using namespace std;

int main()
{
	Mat src1;
	src1 = imread("lena.jpg", CV_LOAD_IMAGE_COLOR);
	namedWindow("Original", CV_WINDOW_AUTOSIZE);
	imshow("Original", src1);

	Mat grey;
	cvtColor(src1, grey, CV_BGR2GRAY);

	Mat sobelx;
	Sobel(grey, sobelx, CV_32F, 1, 0);

	double minVal, maxVal;
	minMaxLoc(sobelx, &minVal, &maxVal); 
	cout << "minVal : " << minVal << endl << "maxVal : " << maxVal << endl;

	Mat draw;
	sobelx.convertTo(draw, CV_8U, 255.0 / (maxVal - minVal), -minVal * 255.0 / (maxVal - minVal));

	namedWindow("sobel", CV_WINDOW_AUTOSIZE);
	imshow("sobel", draw);

	waitKey(0);
	return 0;
}