import cv2
import numpy as np
import dlib
from math import hypot
import pyglet
import time

sound = pyglet.media.load("sound.wav", streaming=False)
left_sound = pyglet.media.load("left.wav", streaming=False)
right_sound = pyglet.media.load("right.wav", streaming=False)

cap = cv2.VideoCapture(0)
board = np.zeros((500, 500), np.uint8)
board[:] = 255

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

keyboard = np.zeros((600, 700, 3), np.uint8)
keys_set_1 = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E",
              5: "F", 6: "G", 7: "H", 8: "I", 9: "J",
              10: "K", 11: "L", 12: "M", 13: "N", 14: "O", 
              15: "P", 16: "Q", 17: "R", 18: "S", 19: "T",
              20: "U", 21: "V", 22: "W", 23: "X", 24: "Y",
              25: "Z"}

def letter(letter_index, text, letter_light):

    if letter_index == 0:
        x = 0
        y = 0
    elif letter_index == 1:
        x = 100
        y = 0
    elif letter_index == 2:
        x = 200
        y = 0
    elif letter_index == 3:
        x = 300
        y = 0
    elif letter_index == 4:
        x = 400
        y = 0
    elif letter_index == 5:
        x = 0
        y = 100
    elif letter_index == 6:
        x = 100
        y = 100
    elif letter_index == 7:
        x = 200
        y = 100
    elif letter_index == 8:
        x = 300
        y = 100
    elif letter_index == 9:
        x = 400
        y = 100
    elif letter_index == 10:
        x = 0
        y = 200
    elif letter_index == 11:
        x = 100
        y = 200
    elif letter_index == 12:
        x = 200
        y = 200
    elif letter_index == 13:
        x = 300
        y = 200
    elif letter_index == 14:
        x = 400
        y = 200
    elif letter_index == 15:
        x = 0
        y = 300
    elif letter_index == 16:
        x = 100
        y = 300    
    elif letter_index == 17:
        x = 200
        y = 300
    elif letter_index == 18:
        x = 300
        y = 300
    elif letter_index == 19:
        x = 400
        y = 300
    elif letter_index == 20:
        x = 0
        y = 400
    elif letter_index == 21:
        x = 100
        y = 400
    elif letter_index == 22:
        x = 200
        y = 400
    elif letter_index == 23:
        x = 300
        y = 400
    elif letter_index == 24:
        x = 400
        y = 400
    elif letter_index == 25:
        x = 0
        y = 500        
    width = 100
    height = 100
    th = 3 
    if letter_light is True:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
    else:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 0, 0), th)


    font_letter = cv2.FONT_HERSHEY_PLAIN
    font_scale = 10
    font_th = 4
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
    cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (255, 0, 0), font_th)

def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

font = cv2.FONT_HERSHEY_PLAIN

def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))


    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_lenght / ver_line_lenght
    return ratio

def get_gaze_ratio(eye_points, facial_landmarks):
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)


    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    gray_eye = eye[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)

    right_side_threshold = threshold_eye[0: height, int(width / 2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)

    if left_side_white == 0:
        gaze_ratio = 1
    elif right_side_white == 0:
        gaze_ratio = 5
    else:
        gaze_ratio = left_side_white / right_side_white
    return gaze_ratio


frames = 0
letter_index = 0
blinking_frames = 0
text = ""
keyboard_selected = "left"
last_keyboard_selected = "left"

while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
    keyboard[:] = (0, 0, 0)
    frames += 1
    new_frame = np.zeros((500, 500, 3), np.uint8)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    active_letter = keys_set_1[letter_index]

    faces = detector(gray)
    for face in faces:


        landmarks = predictor(gray, face)


        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        if blinking_ratio > 5.7:
            cv2.putText(frame, "BLINKING", (50, 150), font, 4, (255, 0, 0), thickness=3)
            blinking_frames += 1
            frames -= 1

            if blinking_frames == 5:
                text += active_letter
                sound.play()
                time.sleep(1)

        else:
            blinking_frames = 0



        gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
        gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
        gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2



        if gaze_ratio <= 0.9:
            keyboard_selected = "right"
            if keyboard_selected != last_keyboard_selected:
                right_sound.play()
                time.sleep(1)
                last_keyboard_selected = keyboard_selected
        else:
            keyboard_selected = "left"
            if keyboard_selected != last_keyboard_selected:
                left_sound.play()
                time.sleep(1)
                last_keyboard_selected = keyboard_selected




    if frames == 26:
        letter_index += 1
        frames = 0
    if letter_index == 26:
        letter_index = 0


    for i in range(26):
        if i == letter_index:
            light = True
        else:
            light = False
        letter(i, keys_set_1[i], light)

    cv2.putText(board, text, (10, 100), font, 4, 0, 3)


    cv2.imshow("Frame", frame)
    cv2.imshow("Virtual keyboard", keyboard)
    cv2.imshow("Board", board)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
