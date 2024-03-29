import json

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
cv2.createTrackbar("1", "Trackbars", 134, 255, nothing)
cv2.createTrackbar("2", "Trackbars", 81, 255, nothing)
cv2.createTrackbar("3", "Trackbars", 118, 255, nothing)
cv2.createTrackbar("4", "Trackbars", 177, 255, nothing)
cv2.createTrackbar("5", "Trackbars", 160, 255, nothing)
cv2.createTrackbar("6", "Trackbars", 194, 255, nothing)

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)


def find_compatible_camera():
    ctx = rs.context()
    devices = ctx.query_devices()
    DS5_product_ids = ["0AD1", "0AD2", "0AD3", "0AD4", "0AD5", "0AF6", "0AFE", "0AFF", "0B00", "0B01", "0B03",
                       "0B07"]
    for dev in devices:
        if dev.supports(rs.camera_info.product_id) and str(
                dev.get_info(rs.camera_info.product_id)) in DS5_product_ids:
            if dev.supports(rs.camera_info.name):
                print("Found device that supports advanced mode:", dev.get_info(rs.camera_info.name))
            return dev
    raise Exception("No device that supports advanced mode was found")


try:
    dev = find_compatible_camera()
    advnc_mode = rs.rs400_advanced_mode(dev)
    while not advnc_mode.is_enabled():
        advnc_mode.toggle_advanced_mode(True)
        time.sleep(2)
        # The 'dev' object will become invalid and we need to initialize it again
        dev = find_compatible_camera()
        advnc_mode = rs.rs400_advanced_mode(dev)

    with open('camera.json', 'r') as f:
        distros_dict = json.load(f)

    as_json_object = json.loads(str(distros_dict).replace("'", '\"'))
    json_string = str(as_json_object).replace("'", '\"')
    advnc_mode.load_json(json_string)

except Exception as e:
    pass
pass

profile = pipeline.start(config)


def basket_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # kernel = np.ones((5, 5), np.uint8)

    # closing = cv2.morphologyEx(hsv, cv2.MORPH_CLOSE, kernel)

    mask = cv2.inRange(hsv, np.array([cv2.getTrackbarPos("1", "Trackbars"), cv2.getTrackbarPos("2", "Trackbars"),
                                      cv2.getTrackbarPos("3", "Trackbars")]),
                       np.array([cv2.getTrackbarPos("4", "Trackbars"), cv2.getTrackbarPos("5", "Trackbars"),
                                 cv2.getTrackbarPos("6", "Trackbars")]))
    #mask = cv2.inRange(hsv, np.array([134, 81, 118]),
    #                   np.array([177, 160, 194]))
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    return opening


def find_blob(blob):  # returns the red colored circle
    largest_contour = 0
    cont_index = 0
    _, contours, hierarchy = cv2.findContours(blob, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > largest_contour:
            largest_contour = area
            cont_index = idx

    if len(contours) > 0:
        r = cv2.boundingRect(contours[cont_index])
        return r[0] + (r[2] / 2), r[3]
    return 0, 0


fps = 0
str_fps = " "
seconds = 0

while True:
    start = time.time()
    frame = pipeline.wait_for_frames()
    depth_frame = frame.get_depth_frame()
    color_frame = frame.get_color_frame()
    frame = np.asanyarray(color_frame.get_data())
    mask = basket_mask(frame)
    x, y = find_blob(mask)
    print(x, y)
    cv2.imshow('Processed', frame)
    cv2.imshow('treshold', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    end = time.time()
    seconds += end - start
    if seconds < 1:
        fps += 1
    elif seconds >= 1:
        seconds = 0
        fps = 0

cv2.destroyAllWindows()
