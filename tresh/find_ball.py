import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("1", "Trackbars", 33, 255, nothing)
cv2.createTrackbar("2", "Trackbars", 142, 255, nothing)
cv2.createTrackbar("3", "Trackbars", 104, 255, nothing)
cv2.createTrackbar("4", "Trackbars", 91, 255, nothing)
cv2.createTrackbar("5", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("6", "Trackbars", 255, 255, nothing)

def get_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_1 = cv2.inRange(hsv, np.array([cv2.getTrackbarPos("1", "Trackbars"), cv2.getTrackbarPos("2", "Trackbars"),
                                        cv2.getTrackbarPos("3", "Trackbars")]),
                         np.array([cv2.getTrackbarPos("4", "Trackbars"), cv2.getTrackbarPos("5", "Trackbars"),
                                   cv2.getTrackbarPos("6", "Trackbars")]))
    mask = mask_1
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    #dilation = cv2.dilate(opening, kernel, iterations=2)
    return opening

index = 565
image = cv2.imread("C:\\Users\\liibepau\\Desktop\\new\\" + str(index) + ".png")
while True:
    cv2.imshow("image", get_mask(image))
    cv2.waitKey(0)
