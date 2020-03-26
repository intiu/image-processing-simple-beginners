#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "iostream"

using namespace cv;
using namespace std;

int main()
{

	Mat image;
	image = imread("lena.jpg", CV_LOAD_IMAGE_COLOR);

	if (!image.data)
	{
		cout << "Could not open or find the image" << std::endl;
		return -1;
	}

	Mat gray;

	cvtColor(image, gray, CV_BGR2GRAY);

	namedWindow("original image", CV_WINDOW_AUTOSIZE);
	imshow("original image", image);

	namedWindow("binary image", CV_WINDOW_AUTOSIZE);
	imshow("binary image", gray);

	waitKey(0);
	return 0;
}