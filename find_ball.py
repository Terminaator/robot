import numpy as np
import cv2
import time
import pyrealsense2 as rs
#from pynput import keyboard

import serial.tools.list_ports
#from pynput.keyboard import Controller

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


def segment_colour(frame):  # returns only the red colors in the frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([cv2.getTrackbarPos("1", "Trackbars"), cv2.getTrackbarPos("2", "Trackbars"),
                                      cv2.getTrackbarPos("3", "Trackbars")]),
                       np.array([cv2.getTrackbarPos("4", "Trackbars"), cv2.getTrackbarPos("5", "Trackbars"),
                                 cv2.getTrackbarPos("6", "Trackbars")]))

    kernel = np.ones((3, 3), np.uint8)
    #opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    #dilation = cv2.dilate(opening, kernel, iterations=2)
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


fps = 0
seconds = 0

while True:
    ##    start = time.time()
    frame = pipeline.wait_for_frames()
    depth_frame = frame.get_depth_frame()
    color_frame = frame.get_color_frame()
    frame = np.asanyarray(color_frame.get_data())
    angle = cv2.getRotationMatrix2D((320, 240), 90, 1)
    frame = cv2.warpAffine(frame, angle, (640, 480))
    ball = segment_colour(frame)
    rec, area = find_blob(ball)
    (x, y, w, h) = rec
    # centre point of the ball
    centre_x = x + ((w) / 2)
    centre_y = y + ((h) / 2)
    u = 2 * (w + h)
    cv2.circle(frame, (int(centre_x), int(centre_y)), 3, (0, 110, 255), -1)
    if 240 < centre_x < 360:
        depth = depth_frame.get_distance(int(centre_x), int(centre_y))
        # u - tuvastatud palli ümber oleva nelinurga ümbermõõt
        print(u)

    cv2.imshow('Processed', frame)
    cv2.imshow('treshold', ball)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
