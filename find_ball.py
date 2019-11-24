import numpy as np
import cv2
import time
import pyrealsense2 as rs
# from pynput import keyboard

import serial.tools.list_ports

# from pynput.keyboard import Controller

ports = serial.tools.list_ports.comports()
device = list(map(lambda port: port.device, ports))[0]

ser = serial.Serial(device, 115200)
throw = False


def nothing(x):
    pass


cv2.namedWindow("Trackbars")
cv2.createTrackbar("1", "Trackbars", 14, 255, nothing)
cv2.createTrackbar("2", "Trackbars", 85, 255, nothing)
cv2.createTrackbar("3", "Trackbars", 76, 255, nothing)
cv2.createTrackbar("4", "Trackbars", 28, 255, nothing)
cv2.createTrackbar("5", "Trackbars", 252, 255, nothing)
cv2.createTrackbar("6", "Trackbars", 189, 255, nothing)

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

profile = pipeline.start(config)
color = profile.get_device().query_sensors()[1]
color.set_option(rs.option.enable_auto_exposure, False)
color.set_option(rs.option.enable_auto_white_balance, False)


def basket_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([167, 173, 207]),
                       np.array([184, 223, 255]))
    return mask


def find_basket(blob):  # returns the red colored circle
    largest_contour = 0
    cont_index = 0
    _, contours, hierarchy = cv2.findContours(blob, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > largest_contour:
            largest_contour = area

            cont_index = idx
    if len(contours) > 0:
        r = cv2.boundingRect(contours[cont_index])
        return r[0], r[2], r[3]
    return 0, 0, 0


while True:
    ##    start = time.time()
    frame = pipeline.wait_for_frames()
    depth_frame = frame.get_depth_frame()
    color_frame = frame.get_color_frame()
    frame = np.asanyarray(color_frame.get_data())
    mask = basket_mask(frame)
    x_start, x_end, y_point = find_basket(mask)
    image = cv2.rectangle(frame, (5, 5), (200, 200), (255, 0, 0), 2)

    cv2.imshow('Processed', frame)
    cv2.imshow('treshold', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
