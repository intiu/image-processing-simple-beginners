#include <iostream>
#include <opencv2\core\core.hpp>
#include <opencv2\highgui\highgui.hpp>
#include <opencv2\imgproc\imgproc.hpp>
#include <opencv2\objdetect\objdetect.hpp>

using namespace cv;
using namespace std;
int main() {
	Mat image;
	vector<Rect> faces;
	CascadeClassifier nhandien;
	VideoCapture camera;
	camera.open(0);				
	nhandien.load("haarcascade_frontalface_alt.xml");
	while (1) {
		camera.read(image);									nhandien.detectMultiScale(image, faces, 1.1, 2, CV_HAAR_SCALE_IMAGE, Size(30, 30));
		if (faces.empty()) {
			cout << "Khong phat hien mat nguoi!" << endl;
		}
		for (int i = 0; i < faces.size(); ++i)
			rectangle(image, faces.at(i), CV_RGB(200, 0, 0), 2);
		cout << "So mat phat hien duoc: " << faces.size() << endl;
		imshow("PHAT HIEN GUONG MAT", image);
		cvWaitKey(10);
	}
	waitKey(0);
}