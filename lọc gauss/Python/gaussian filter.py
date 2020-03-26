import cv2
import numpy
src = cv2.imread('lena.jpg', cv2.IMREAD_UNCHANGED)
dst = cv2.GaussianBlur(src,(5,5),cv2.BORDER_DEFAULT)
cv2.imshow("Gaussian Smoothing",numpy.hstack((src, dst)))
cv2.waitKey(0)
cv2.destroyAllWindows() 
