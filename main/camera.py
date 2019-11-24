import json
import cv2
from imageProccessing import configuration
import numpy as np
import pyrealsense2 as rs
import time


class vision:

    def __init__(self):
        conf = configuration.configuration()
        self.ball_color_range = conf.get("colors", conf.get("vision", "ball_color"))
        self.ball_noise_kernel = conf.get("vision", "ball_noise_kernel")
        self.blue_basket_color_range = conf.get("colors", conf.get("vision", "blue_basket_color"))
        self.magenta_basket_color_range = conf.get("colors", conf.get("vision", "magenta_basket_color"))

    def find_compatible_camera(self):
        ctx = rs.context()
        ds5_dev = rs.device()
        devices = ctx.query_devices();
        DS5_product_ids = ["0AD1", "0AD2", "0AD3", "0AD4", "0AD5", "0AF6", "0AFE", "0AFF", "0B00", "0B01", "0B03",
                           "0B07"]
        for dev in devices:
            if dev.supports(rs.camera_info.product_id) and str(
                    dev.get_info(rs.camera_info.product_id)) in DS5_product_ids:
                if dev.supports(rs.camera_info.name):
                    print("Found device that supports advanced mode:", dev.get_info(rs.camera_info.name))
                return dev
        raise Exception("No device that supports advanced mode was found")

    def configure_rs_camera(self):
        try:
            dev = self.find_compatible_camera()
            advnc_mode = rs.rs400_advanced_mode(dev)
            while not advnc_mode.is_enabled():
                advnc_mode.toggle_advanced_mode(True)
                time.sleep(2)
                # The 'dev' object will become invalid and we need to initialize it again
                dev = self.find_compatible_camera()
                advnc_mode = rs.rs400_advanced_mode(dev)

            with open('custompreset.json', 'r') as f:
                distros_dict = json.load(f)

            as_json_object = json.loads(str(distros_dict).replace("'", '\"'))
            json_string = str(as_json_object).replace("'", '\"')
            advnc_mode.load_json(json_string)

        except Exception as e:
            print(e)
        pass

    def apply_ball_color_filter(self, hsv):
        # Apply ball color filter
        mask = cv2.inRange(hsv, self.ball_color_range["min"], self.ball_color_range["max"])

        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return opening

    def apply_basket_color_filter(self, hsv, color):
        # Apply ball color filter
        if (color == "blue"):
            mask = cv2.inRange(hsv, self.blue_basket_color_range["min"], self.blue_basket_color_range["max"])
            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        elif (color == "magenta"):
            mask = cv2.inRange(hsv, self.magenta_basket_color_range["min"], self.magenta_basket_color_range["max"])
            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return opening

    def detect_ball(self, mask_in, mask):
        _,contours, _ = cv2.findContours(mask_in, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_list = []

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            closest_ball = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(closest_ball)
            if area > 10:
                contour_list.append(contour)
                rect = cv2.minAreaRect(closest_ball)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                cv2.drawContours(mask, [box],0, (50, 100, 200), 2)
                x_coordinate = rect[0][0]
                y_coordinate = rect[0][1]

                return x_coordinate, y_coordinate
        return -1, -1

    def detect_basket(self, in_mask, out_mask):

        _,contours, _ = cv2.findContours(in_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:

            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h
            if aspect_ratio < 3.5:
                rect = cv2.minAreaRect(cnt)
                x_coordinate = rect[0][0]
                y_coordinate = rect[1][0]
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                im = cv2.drawContours(out_mask, [box], 0, (100, 100, 100), 5)
                area = cv2.contourArea(cnt)
                return x_coordinate, y_coordinate
        return -1,-1

    def calculate_distance_with_buffer(self, queue):
        average = np.mean(queue)
        return average