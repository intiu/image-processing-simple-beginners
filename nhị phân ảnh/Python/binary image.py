import cv2 
import numpy 
img = cv2.imread('download.jpg',0)
ret,gray=cv2.threshold(img,127,256,cv2.THRESH_BINARY)
cv2.imshow('orginal image',img)
cv2.imshow('binary image',gray)
cv2.waitKey(0)
cv2.DestroyAllWindows()
