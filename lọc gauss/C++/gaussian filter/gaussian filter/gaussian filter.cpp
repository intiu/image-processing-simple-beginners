#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui_c.h>
using namespace cv;
int main(int argc, char** argv)
{
	namedWindow("original", CV_WINDOW_AUTOSIZE);
	Mat src = imread("lena.jpg", 1);
	Mat dst;
	imshow("original", src);
	for (int i = 1; i < 51; i = i + 2)
	{
		GaussianBlur(src, dst, Size(i, i), 0, 0);
		imshow("Gaussian filter", dst);
		waitKey(5000);
	}
}