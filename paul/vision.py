import json
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

        self.frame = None
        try:
            dev = self.find_camera()
            advnc_mode = rs.rs400_advanced_mode(dev)
            while not advnc_mode.is_enabled():
                advnc_mode.toggle_advanced_mode(True)
                time.sleep(2)
                # The 'dev' object will become invalid and we need to initialize it again
                dev = self.find_camera()
                advnc_mode = rs.rs400_advanced_mode(dev)

            with open('camera.json', 'r') as f:
                distros_dict = json.load(f)

            as_json_object = json.loads(str(distros_dict).replace("'", '\"'))
            json_string = str(as_json_object).replace("'", '\"')
            advnc_mode.load_json(json_string)

        except Exception as e:
            pass
        self.profile = self.pipeline.start(self.config)

    def find_camera(self):
        ctx = rs.context()
        devices = ctx.query_devices()
        products = ["0AD1", "0AD2", "0AD3", "0AD4", "0AD5", "0AF6", "0AFE", "0AFF", "0B00", "0B01", "0B03",
                    "0B07"]
        for dev in devices:
            if dev.supports(rs.camera_info.product_id) and str(
                    dev.get_info(rs.camera_info.product_id)) in products:
                if dev.supports(rs.camera_info.name):
                    print("Found device that supports advanced mode:", dev.get_info(rs.camera_info.name))
                return dev
        raise Exception("No device that supports advanced mode was found")

    def on_message(self, msg):
        print("vision received:", msg)

    def mask(self, frame, ball):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        if ball:
            mask = cv2.inRange(hsv, np.array([15, 15, 68]),
                               np.array([95, 226, 228]))
        else:
            mask = cv2.inRange(hsv, np.array([134, 81, 118]),
                               np.array([177, 160, 194]))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        return opening

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
            if ball:
                return r[0] + (r[2] / 2), r[1] + (r[3] / 2)
            else:
                return r[0] + (r[2] / 2), r[3]
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

        cv2.imshow('frame', self.ball_mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return


vision = Vision()
cv2.destroyAllWindows()
