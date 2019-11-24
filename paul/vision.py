import time

import pyrealsense2 as rs
import cv2
import numpy as np

from ai import ai
from thread import Thread


class Vision(Thread):
    def __init__(self, ):
        Thread.__init__(self)
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

        self.profile = self.pipeline.start(self.config)
        self.frame = None
        camera_one = self.profile.get_device().query_sensors()[1]
        camera_one.set_option(rs.option.enable_auto_exposure, False)
        camera_one.set_option(rs.option.enable_auto_white_balance, False)

    def on_message(self, msg):
        print("vision received:", msg)

    def mask(self, frame, ball):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        if ball:
            mask = cv2.inRange(hsv, np.array([14, 85, 76]),
                               np.array([28, 252, 189]))
            mask = cv2.dilate(mask,  np.ones((3, 3), np.uint8), iterations=10)
        else:
            mask = cv2.inRange(hsv, np.array([167, 173, 207]),
                               np.array([184, 223, 255]))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        return mask

    def read_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        return depth_frame, color_frame

    def find_blob(self, blob, ball):  # returns the red colored circle
        largest_contour = 0
        cont_index = 0
        if ball:
            _, contours, hierarchy = cv2.findContours(blob, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        else:
            _, contours, hierarchy = cv2.findContours(blob, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for idx, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > largest_contour:
                largest_contour = area

                cont_index = idx
        if len(contours) > 0:
            r = cv2.boundingRect(contours[cont_index])

            return r[0] + (r[2] / 2), r[1] + (r[3] / 2)
        return 0, 0

    def on_tick(self):
        depth_frame, color_frame = self.read_frame()
        if not depth_frame or not color_frame:
            return
        self.frame = np.asanyarray(color_frame.get_data())
        ball_mask = self.mask(self.frame, True)
        basket_mask = self.mask(self.frame, False)
        x_ball, y_ball = self.find_blob(ball_mask, True)
        x_basket, y_basket = self.find_blob(basket_mask, False)
        ai.send_message({
            "ball_coordinates": (x_ball, y_ball),
            "basket_coordinates": (x_basket, y_basket),
            "ball_distance": (depth_frame.get_distance(int(x_ball), int(y_ball))),
            "basket_distance": (depth_frame.get_distance(int(x_basket), int(y_basket)))
        })


vision = Vision()
