import numpy as np
import cv2
import time
import pyrealsense2 as rs

# open the camera
# cap = cv2.VideoCapture(1)

def nothing(x):
    pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("1", "Trackbars", 67, 255, nothing)
cv2.createTrackbar("2", "Trackbars", 122, 255, nothing)
cv2.createTrackbar("3", "Trackbars", 60, 255, nothing)
cv2.createTrackbar("4", "Trackbars", 91, 255, nothing)
cv2.createTrackbar("5", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("6", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("7", "Trackbars", 165, 255, nothing)
cv2.createTrackbar("8", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("9", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("10", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("11", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("12", "Trackbars", 255, 255, nothing)


pipeline = rs.pipeline()
config = rs.config()

# config.enable_device('801212070130')

# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 320, 240, rs.format.bgr8, 60)

profile = pipeline.start(config)


# profile = pipeline.start()

def segment_colour(frame):  # returns only the red colors in the frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_1 = cv2.inRange(hsv, np.array([cv2.getTrackbarPos("1", "Trackbars"), cv2.getTrackbarPos("2", "Trackbars"),
                                            cv2.getTrackbarPos("3", "Trackbars")]),
                         np.array([cv2.getTrackbarPos("4", "Trackbars"), cv2.getTrackbarPos("5", "Trackbars"),
                                   cv2.getTrackbarPos("6", "Trackbars")]))
    ycr_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    mask_2 = cv2.inRange(ycr_roi, np.array([cv2.getTrackbarPos("7", "Trackbars"), cv2.getTrackbarPos("8", "Trackbars"),
                                            cv2.getTrackbarPos("9", "Trackbars")]),
                         np.array([cv2.getTrackbarPos("10", "Trackbars"), cv2.getTrackbarPos("11", "Trackbars"),
                                   cv2.getTrackbarPos("12", "Trackbars")]))

    mask = mask_1 | mask_2
    kern_dilate = np.ones((8, 8), np.uint8)
    kern_erode = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kern_erode)  # Eroding
    mask = cv2.dilate(mask, kern_dilate)  # Dilating
    return mask


def find_blob(blob):  # returns the red colored circle
    largest_contour = 0
    cont_index = 0
    _,contours, hierarchy = cv2.findContours(blob, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > largest_contour):
            largest_contour = area

            cont_index = idx
            k = cv2.isContourConvex(contour)
            if k and 10 < len(contour) < 20:
                cont_index=idx
    r = (0, 0, 2, 2)
    if len(contours) > 0:
        r = cv2.boundingRect(contours[cont_index])

    return r, largest_contour


while True:

    start = time.time()
    frame = pipeline.wait_for_frames()
    color_frame = frame.get_color_frame()
    frame = np.asanyarray(color_frame.get_data())
    cv2.getTrackbarPos("1", "Trackbars")
    ball = segment_colour(frame)
    rec, area = find_blob(ball)
    (x, y, w, h) = rec
    if (w * h) < 10:
        found = 0
    else:
        found = 1
        simg2 = cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
        centre_x = x + ((w) / 2)
        centre_y = y + ((h) / 2)
        if 280 < centre_x < 360:
            print(centre_x)
        cv2.circle(frame, (int(centre_x), int(centre_y)), 3, (0, 110, 255), -1)
        centre_x -= 80
        centre_y = 6 - -centre_y
    cv2.imshow('Processed', frame)
    cv2.imshow('treshold', ball)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
# cap.release()
cv2.destroyAllWindows()
