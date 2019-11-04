import numpy as np
import cv2
import time
import pyrealsense2 as rs
import serial.tools.list_ports

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

profile = pipeline.start(config)
ports = serial.tools.list_ports.comports()
device = list(map(lambda port: port.device, ports))[0]

ser = serial.Serial(device, 115200)


def on_press(k):
    global throw
    if k == 'up':
        if throw:
            ser.write("sd:0:-10:10\nd:1500\n".encode())
        ser.write("sd:0:-10:10\n".encode())
    elif k == 'left':
        if throw:
            ser.write("sd:0:-10:-10\nd:1500\n".encode())
        ser.write("sd:0:-10:-10\n".encode())
    elif k == 'down':
        if throw:
            ser.write("sd:0:10:-10\nd:1500\n".encode())
        ser.write("sd:0:10:-10\n".encode())
    elif k == 'right':
        if throw:
            ser.write("sd:0:10:10\nd:1500\n".encode())
        ser.write("sd:0:10:10\n".encode())


def find_blob(blob):  # returns the red colored circle
    largest_contour = 0
    cont_index = 0
    _, contours, hierarchy = cv2.findContours(blob, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > largest_contour):
            largest_contour = area
            cont_index = idx
    r = (0, 0, 2, 2)
    if len(contours) > 0:
        r = cv2.boundingRect(contours[cont_index])

    return r, largest_contour


def read_frame():
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    return (color_frame, depth_frame)


def segment_colour(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_1 = cv2.inRange(hsv, np.array([33, 142, 104]),
                         np.array([91, 255, 255]))
    mask = mask_1
    kern_dilate = np.ones((3, 3), np.uint8)
    kern_erode = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kern_erode)  # Eroding
    mask = cv2.dilate(mask, kern_dilate)  # Dilating
    return mask


frames = [None, None, None]
while True:
    color_frame, depth_frame = read_frame()
    frame = np.asanyarray(color_frame.get_data())
    if frames[0] is not None:
        frames[0] = frame
    elif frames[1] is not None:
        frames[1] = frame
    elif frames[2] is not None:
        frames[2] = frame

    if frames[0] is not None and frames[1] is not None and frames[2] is not None:
        frame = cv2.bitwise_and(frames[0], frames[1])
        frame = cv2.bitwise_and(frame, frames[2])
        ball_treshold = segment_colour(frame)
        (x, y, w, h), area = find_blob(ball_treshold)
        if (w * h) < 10:
            on_press("up")
        cv2.imshow('Processed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
