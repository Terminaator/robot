from threading import Thread

import cv2
import numpy as np
import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

profile = pipeline.start(config)

frame = None

def mask():
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_1 = cv2.inRange(hsv, np.array([33,142,104]),
                         np.array([91,255,255]))
    ycr_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

    mask = mask_1
    kern_dilate = np.ones((3, 3), np.uint8)
    kern_erode = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kern_erode)
    mask = cv2.dilate(mask, kern_dilate)
    return mask

def get_frame():
    while True:
        global frame
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        frame = np.asanyarray(color_frame.get_data())

if __name__ == "__main__":
    t1 = Thread(target=get_frame)
    t1.setDaemon(True)
    t1.start()
    while True:
        print(2)
        if frame is not None:
            cv2.imshow('Processed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
