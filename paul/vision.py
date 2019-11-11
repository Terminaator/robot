import pyrealsense2 as rs
import cv2
import numpy as np

from thread import Thread


class Vision(Thread):
    def __init__(self, ):
        Thread.__init__(self)
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

        self.profile = self.pipeline.start(self.config)

    def on_message(self, msg):
        print("vision received:", msg)

    def ball_mask(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([33, 142, 104]),
                           np.array([91, 255, 255]))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        return opening

    def read_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        return depth_frame, color_frame

    def find_ball(self, blob):  # returns the red colored circle
        largest_contour = 0
        cont_index = 0
        _, contours, hierarchy = cv2.findContours(blob, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        for idx, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > largest_contour):
                largest_contour = area

                cont_index = idx
        if len(contours) > 0:
            r = cv2.boundingRect(contours[cont_index])

            return r[0] + (r[2] / 2), r[1] + (r[3] / 2)

        return 0,0

    def on_tick(self):
        depth_frame, color_frame = self.read_frame()
        if not depth_frame or not color_frame:
            return
        frame_wrong_way = np.asanyarray(color_frame.get_data())
        frame = cv2.warpAffine(frame_wrong_way, cv2.getRotationMatrix2D((320, 240), 90, 1), (640, 480))
        ball_mask = self.ball_mask(frame)
        ball_x,ball_y = self.find_ball(ball_mask)
        cv2.imshow('Processed', ball_mask)
        print(ball_x, ball_y)