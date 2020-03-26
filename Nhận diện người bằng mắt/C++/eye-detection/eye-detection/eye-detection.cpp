#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;


void fillHoles(Mat &mask)
{
	Mat maskFloodfill = mask.clone();
	floodFill(maskFloodfill, cv::Point(0, 0), Scalar(255));
	Mat mask2;
	bitwise_not(maskFloodfill, mask2);
	mask = (mask2 | mask);

}

int main(int argc, char** argv)
{
	Mat img = imread("red_eyes2.jpg", CV_LOAD_IMAGE_COLOR);
	Mat imgOut = img.clone();
	CascadeClassifier eyesCascade("haarcascade_eye.xml");
	std::vector<Rect> eyes;
	eyesCascade.detectMultiScale(img, eyes, 1.3, 4, 0 | CASCADE_SCALE_IMAGE, Size(100, 100));
	for (size_t i = 0; i < eyes.size(); i++)
	{
		Mat eye = img(eyes[i]);
		vector<Mat>bgr(3);
		split(eye, bgr);
		Mat mask = (bgr[2] > 150) & (bgr[2] > (bgr[1] + bgr[0]));
		fillHoles(mask);
		dilate(mask, mask, Mat(), Point(-1, -1), 3, 1, 1);
		Mat mean = (bgr[0] + bgr[1]) / 2;
		mean.copyTo(bgr[2], mask);
		mean.copyTo(bgr[0], mask);
		mean.copyTo(bgr[1], mask);
		Mat eyeOut;
		cv::merge(bgr, eyeOut);
		eyeOut.copyTo(imgOut(eyes[i]));

	}
	imshow("Red Eyes", img);
	imshow("original ", imgOut);
	waitKey(0);

}