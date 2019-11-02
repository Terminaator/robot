import cv2
import numpy as np

location = "C://Users//liibepau//Desktop//Pall//"


def nothing(x):
    pass
cv2.namedWindow("Trackbars")
cv2.createTrackbar("1", "Trackbars", 38, 255, nothing)
cv2.createTrackbar("2", "Trackbars", 102, 255, nothing)
cv2.createTrackbar("3", "Trackbars", 53, 255, nothing)
cv2.createTrackbar("4", "Trackbars", 80, 255, nothing)
cv2.createTrackbar("5", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("6", "Trackbars", 182, 255, nothing)
cv2.createTrackbar("7", "Trackbars", 165, 255, nothing)
cv2.createTrackbar("8", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("9", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("10", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("11", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("12", "Trackbars", 255, 255, nothing)

def segment_colour(frame):  # returns only the red colors in the frame
    hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_1 = cv2.inRange(hsv_roi, np.array([cv2.getTrackbarPos("1", "Trackbars"), cv2.getTrackbarPos("2", "Trackbars"),
                                            cv2.getTrackbarPos("3", "Trackbars")]),
                         np.array([cv2.getTrackbarPos("4", "Trackbars"), cv2.getTrackbarPos("5", "Trackbars"),
                                   cv2.getTrackbarPos("6", "Trackbars")]))
    ycr_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    mask_2 = cv2.inRange(ycr_roi, np.array([cv2.getTrackbarPos("7", "Trackbars"), cv2.getTrackbarPos("8", "Trackbars"),
                                            cv2.getTrackbarPos("9", "Trackbars")]),
                         np.array([cv2.getTrackbarPos("10", "Trackbars"), cv2.getTrackbarPos("11", "Trackbars"),
                                   cv2.getTrackbarPos("12", "Trackbars")]))
    mask = mask_1 | mask_2
    #kern_dilate = np.ones((8, 8), np.uint8)
    #kern_erode = np.ones((3, 3), np.uint8)
    #mask = cv2.erode(mask, kern_erode)  # Eroding
    #mask = cv2.dilate(mask, kern_dilate)  # Dilating
    return mask


img = cv2.imread(location, -1)

while True:
    ball = segment_colour(img)
    cv2.imshow('ball', ball)
    if cv2.waitKey(0):
        break
cv2.destroyAllWindows()