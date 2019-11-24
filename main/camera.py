import threading

import cv2
import numpy as np
import pyrealsense2 as rs

pipeline = rs.pipeline()

config = rs.config()

config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 60)

profile = pipeline.start(config)

color = profile.get_device().query_sensors()[1]
color.set_option(rs.option.enable_auto_exposure, False)

color.set_option(rs.option.enable_auto_white_balance, False)

def nothing(x):
    pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("1", "Trackbars", 40, 255, nothing)
cv2.createTrackbar("2", "Trackbars", 73, 255, nothing)
cv2.createTrackbar("3", "Trackbars", 66, 255, nothing)
cv2.createTrackbar("4", "Trackbars", 80, 255, nothing)
cv2.createTrackbar("5", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("6", "Trackbars", 255, 255, nothing)

def ball_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([cv2.getTrackbarPos("1", "Trackbars"), cv2.getTrackbarPos("2", "Trackbars"),
                                      cv2.getTrackbarPos("3", "Trackbars")]),
                       np.array([cv2.getTrackbarPos("4", "Trackbars"), cv2.getTrackbarPos("5", "Trackbars"),
                                 cv2.getTrackbarPos("6", "Trackbars")]))
    kernel = np.ones((8, 8), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    dilation = cv2.dilate(opening, kernel, iterations=2)

    return mask

while True:
    frame = pipeline.wait_for_frames()
    color_frame = frame.get_color_frame()
    frame = np.asanyarray(color_frame.get_data())
    cv2.imshow('Processed', ball_mask(frame))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
