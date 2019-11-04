from threading import Thread

import cv2
import numpy as np
import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

profile = pipeline.start(config)

frame = None


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
        cv2.imshow('Processed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
