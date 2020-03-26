import cv2
 
def save_webcam(outPath,fps,mirror=False):
    cap = cv2.VideoCapture(0)
    currentFrame = 0
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)    
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)   
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(outPath, fourcc, fps, (int(width), int(height)))
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            if mirror == True:
                frame = cv2.flip(frame, 1)
            out.write(frame)            
            cv2.imshow('camera', frame)
        else:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break
        currentFrame += 1     
    cap.release()
    out.release()
    cv2.destroyAllWindows() 
def main():
    save_webcam('mouthwash.avi', 5.0,mirror=True) 
if __name__ == '__main__':
    main()
