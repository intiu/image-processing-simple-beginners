import cv2
import numpy as np
import imutils
from pynput.mouse import Button, Controller
import wx

mouse=  Controller()

app = wx.App(False)
(sx,sy) = wx.GetDisplaySize()
(camx,camy) = (420,340)


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

min_YCrCb = np.array([0, 131, 100],np.uint8)
max_YCrCb = np.array([255, 185, 135],np.uint8)

kernelopen= np.ones((1,1))
kernelclose= np.ones((1,1))

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

fgbg = cv2.createBackgroundSubtractorMOG2(history = 20, varThreshold =25)

cam = cv2.VideoCapture(0)
cam.set(3,camx)
cam.set(4,camy)


while True:

    ret, img = cam.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for(x,y,w,h) in faces :
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,0), -1)
    
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

    

    imageYCrCb = cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)
    skinRegion = cv2.inRange(imageYCrCb,min_YCrCb,max_YCrCb)

    maskopen = cv2.morphologyEx(skinRegion,cv2.MORPH_OPEN, kernelopen)
    maskclose = cv2.morphologyEx(maskopen,cv2.MORPH_OPEN, kernelclose)
    contours, hierarchy = cv2.findContours(maskclose.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnt = max(contours, key=lambda x:cv2.contourArea(x))

    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(img,(x,y), (x+w, y+h-40), (0,0,255), 0)
       
    hull = cv2.convexHull(cnt)

    drawing = np.zeros(img.shape, np.uint8)
    cv2.drawContours(drawing, [cnt], -1, (0,255,0), 0)
    cv2.drawContours(drawing, [hull], -1, (0,0,255), 0)

    cx = x+w//2
    cy = y+h//2
    cv2.circle(img,(cx,cy),2,(255,0,0),2)

    mouse.position = (sx-(cx*sx//camx), cy*sy//camy)
    while mouse.position != (sx-(cx*sx//camx), cy*sy//camy):
        pass
  
    cv2.imshow('img',img)
    cv2.imshow("maskclose",maskclose)
    all_img = np.hstack((drawing, img))
    cv2.imshow('last', all_img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
 
cv2.destroyAllWindows()
cam.release()

