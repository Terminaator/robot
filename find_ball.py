import numpy as np
import cv2
import time
import pyrealsense2 as rs


def nothing(x):
    pass


cv2.namedWindow("Trackbars")
cv2.createTrackbar("1", "Trackbars", 33, 255, nothing)
cv2.createTrackbar("2", "Trackbars", 142, 255, nothing)
cv2.createTrackbar("3", "Trackbars", 104, 255, nothing)
cv2.createTrackbar("4", "Trackbars", 91, 255, nothing)
cv2.createTrackbar("5", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("6", "Trackbars", 255, 255, nothing)

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 30)

profile = pipeline.start(config)


def segment_colour(frame):  # returns only the red colors in the frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([cv2.getTrackbarPos("1", "Trackbars"), cv2.getTrackbarPos("2", "Trackbars"),
                                        cv2.getTrackbarPos("3", "Trackbars")]),
                         np.array([cv2.getTrackbarPos("4", "Trackbars"), cv2.getTrackbarPos("5", "Trackbars"),
                                   cv2.getTrackbarPos("6", "Trackbars")]))
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return opening


def find_blob(blob):  # returns the red colored circle
    largest_contour = 0
    cont_index = 0
    _, contours, hierarchy = cv2.findContours(blob, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > largest_contour):
            largest_contour = area

            cont_index = idx
            k = cv2.isContourConvex(contour)
            if k and 10 < len(contour) < 20:
                cont_index = idx
    r = (0, 0, 2, 2)
    if len(contours) > 0:
        r = cv2.boundingRect(contours[cont_index])

    return r, largest_contour



while True:
    start = time.time()
    frame = pipeline.wait_for_frames()
    depth_frame = frame.get_depth_frame()
    color_frame = frame.get_color_frame()
    if not depth_frame:
        continue
    frame = np.asanyarray(color_frame.get_data())
    frame = cv2.warpAffine(frame, cv2.getRotationMatrix2D((360, 240), 90, 1), (720, 480))
    ball = segment_colour(frame)

    rec, area = find_blob(ball)
    (x, y, w, h) = rec
    if (w * h) < 10:
        None
    else:
        simg2 = cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
        centre_x = x + (w / 2)
        centre_y = y + (h / 2)
        zDepth = depth_frame.get_distance(int(centre_x), int(centre_y))
        print(zDepth)
        cv2.circle(frame, (int(centre_x), int(centre_y)), 3, (0, 110, 255), -1)
    cv2.imshow('Processed', frame)
    cv2.imshow('treshold', ball)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
