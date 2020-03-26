#include <opencv2\highgui\highgui.hpp>
#include<iostream>
using namespace cv;
using namespace std;
int main() {
	char *DD = new char[100];	
	cout << "Nhap duong dan: "; 	cin >> DD;
	Mat image;			
	image = imread(DD);	
	if (!image.data) {	
		cout << "Khong the tim thay anh";
		system("pause");
		exit(0);
	}
	namedWindow("PICTURE", WINDOW_NORMAL);
	imshow("PICTURE", image);
	waitKey(0);
}