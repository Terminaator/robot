import threading

import numpy as np
import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

profile = pipeline.start(config)


def get_frame():
    frame = pipeline.wait_for_frames()
    color_frame = frame.get_color_frame()
    frame = np.asanyarray(color_frame.get_data())
    return frame


thread1 = threading.Thread(get_frame())
thread1.start()
thread1.join()
