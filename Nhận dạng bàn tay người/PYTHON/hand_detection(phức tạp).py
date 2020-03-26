#Include file haarcascade_frontalface_default.xml

import cv2
import numpy as np
import imutils

import math

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#YCrCb = Y:luminance component , Cr:red chrominat, Cb:blue chrominant
min_YCrCb = np.array([0, 131, 100],np.uint8)
max_YCrCb = np.array([255, 185, 135],np.uint8)

kernelopen= np.ones((1,1))
kernelclose= np.ones((1,1))

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

fgbg = cv2.createBackgroundSubtractorMOG2(history = 20, varThreshold =25)

cap = cv2.VideoCapture(0)

while True:

    ret, img = cap.read()
    img = cv2.resize(img,(340,220))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for(x,y,w,h) in faces :
        cv2.rectangle(img, (x,y-20), (x+w,y+h+50), (0,0,0), -1)
    
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

    

    imageYCrCb = cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)
    skinRegion = cv2.inRange(imageYCrCb,min_YCrCb,max_YCrCb)

    maskopen = cv2.morphologyEx(skinRegion,cv2.MORPH_OPEN, kernelopen)
    maskclose = cv2.morphologyEx(maskopen,cv2.MORPH_OPEN, kernelclose)
    contours, hierarchy = cv2.findContours(maskclose.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    try:
        cnt = max(contours, key=lambda x:cv2.contourArea(x))

        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x,y), (x+w, y+h), (0,0,255), 0)
       
        hull = cv2.convexHull(cnt)

        drawing = np.zeros(img.shape, np.uint8)
        cv2.drawContours(drawing, [cnt], -1, (0,255,0), 0)
        cv2.drawContours(drawing, [hull], -1, (0,0,255), 0)

        hull = cv2.convexHull(cnt, returnPoints=False)
        defects = cv2.convexityDefects(cnt,hull)

        d=0

        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])

            a=math.sqrt((end[0] - start[0]) **2 + (end[1] - start[1])**2)
            b=math.sqrt((far[0] - start[0]) **2 + (far[1] - start[1])**2)
            c=math.sqrt((end[0] - far[0]) **2 + (end[1] - far[1])**2)

            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))

            d = (2*ar)/a

            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c))*57
          #if angle <= 90 :  (it gives all the defects far,end and start)
            if angle <= 90 and d>30:
                d+=1
                cv2.circle(img, far, 3, [0,0,255],-1)
            cv2.line(img, start, end, [0,255,0], 2)

        FONT = cv2.FONT_HERSHEY_SIMPLEX
        if d == 4:
            cv2.putText(img, "5", (0, 50), FONT, 2,(0,0,255), 2)
        else:
            pass            
    except:
        pass

  
    cv2.imshow('img',img)
    cv2.imshow("maskclose",maskclose)
    all_img = np.hstack((drawing, img))
    cv2.imshow('last', all_img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
 
cv2.destroyAllWindows()
cap.release()

#Tankyou :)
