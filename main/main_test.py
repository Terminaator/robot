import numpy as np
import cv2
import time
import pyrealsense2 as rs
from pynput import keyboard

import serial.tools.list_ports
from pynput.keyboard import Controller

ports = serial.tools.list_ports.comports()
device = list(map(lambda port: port.device, ports))[0]

ser = serial.Serial(device, 115200)
throw = False
def on_press(k):
    global throw
    if k == 'up':
        if throw:
            ser.write("sd:0:-10:10\nd:1500\n".encode())
        ser.write("sd:0:-10:10\n".encode())
    elif k == 'left':
        if throw:
            ser.write("sd:0:-5:-5\nd:1500\n".encode())
        ser.write("sd:0:-5:-5\n".encode())
    elif k == 'down':
        if throw:
            ser.write("sd:0:10:-10\nd:1500\n".encode())
        ser.write("sd:0:10:-10\n".encode())
    elif k == 'right':
        if throw:
            ser.write("sd:0:5:5\nd:1500\n".encode())
        ser.write("sd:0:5:5\n".encode())
    elif k == 'space':
        if throw:
            ser.write("sd:0:0:0\nd:1500\n".encode())
        ser.write("sd:0:0:0\n".encode())
    elif k == 'e':
        if throw:
            ser.write("sd:10:0:0\nd:1500\n".encode())
        ser.write("sd:10:0:0\n".encode())
    elif k == 'q':
        if throw:
            ser.write("sd:-10:0:0\nd:1500\n".encode())
        ser.write("sd:-10:0:0\n".encode())
    elif k == 'd':
        if throw:
            throw = False
        else:
            throw = True



#lis = keyboard.Listener(on_press=on_press)
#lis.start()

#lis.join()

def nothing(x):
    pass


cv2.namedWindow("Trackbars")
cv2.createTrackbar("1", "Trackbars", 33, 255, nothing)
cv2.createTrackbar("2", "Trackbars", 142, 255, nothing)
cv2.createTrackbar("3", "Trackbars", 104, 255, nothing)
cv2.createTrackbar("4", "Trackbars", 91, 255, nothing)
cv2.createTrackbar("5", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("6", "Trackbars", 255, 255, nothing)

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

profile = pipeline.start(config)


def segment_colour(frame):  # returns only the red colors in the frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_1 = cv2.inRange(hsv, np.array([cv2.getTrackbarPos("1", "Trackbars"), cv2.getTrackbarPos("2", "Trackbars"),
                                        cv2.getTrackbarPos("3", "Trackbars")]),
                         np.array([cv2.getTrackbarPos("4", "Trackbars"), cv2.getTrackbarPos("5", "Trackbars"),
                                   cv2.getTrackbarPos("6", "Trackbars")]))

    mask = mask_1  # | mask_2
    kern_dilate = np.ones((3, 3), np.uint8)
    kern_erode = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kern_erode)  # Eroding
    mask = cv2.dilate(mask, kern_dilate)  # Dilating
    return mask


def find_blob(blob):  # returns the red colored circle
    largest_contour = 0
    cont_index = 0
    _, contours, hierarchy = cv2.findContours(blob, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > largest_contour):
            largest_contour = area

            cont_index = idx
            k = cv2.isContourConvex(contour)
            if k and 10 < len(contour) < 20:
                cont_index = idx
    r = (0, 0, 2, 2)
    if len(contours) > 0:
        r = cv2.boundingRect(contours[cont_index])

    return r, largest_contour



while True:
    frame = pipeline.wait_for_frames()
    color_frame = frame.get_color_frame()
    frame = np.asanyarray(color_frame.get_data())
    angle = cv2.getRotationMatrix2D((320,240), 90, 1)
    frame = cv2.warpAffine(frame, angle, (640,480))
    ball = segment_colour(frame)
    rec, area = find_blob(ball)
    (x, y, w, h) = rec
    # centre point of the ball
    centre_x = x + ((w) / 2)
    centre_y = y + ((h) / 2)
    cv2.circle(frame, (int(centre_x), int(centre_y)), 3, (0, 110, 255), -1)
    if 280 < centre_x < 320:
        on_press("space")
        if (w * h) > 20:
            # stay still
            on_press("space")
        else:
            print("up")
            on_press("up")
    else:
        on_press("left")
    cv2.imshow('Processed', frame)
    cv2.imshow('treshold', ball)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
