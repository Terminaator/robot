import numpy as np
import cv2
import time
import pyrealsense2 as rs

# open the camera
# cap = cv2.VideoCapture(1)
trackbar_value = 69
trackbar_value1 = 145
trackbar_value2 = 131
trackbar_value3 = 81
trackbar_value4 = 240
trackbar_value5 = 208


def updateValue(new_value):
    # make sure to write the new value into the global variable
    global trackbar_value
    trackbar_value = new_value
    return


def updateValue1(new_value):
    # make sure to write the new value into the global variable
    global trackbar_value1
    trackbar_value1 = new_value
    return


def updateValue2(new_value):
    # make sure to write the new value into the global variable
    global trackbar_value2
    trackbar_value2 = new_value
    return


def updateValue3(new_value):
    # make sure to write the new value into the global variable
    global trackbar_value3
    trackbar_value3 = new_value
    return


def updateValue4(new_value):
    # make sure to write the new value into the global variable
    global trackbar_value4
    trackbar_value4 = new_value
    return


def updateValue5(new_value):
    # make sure to write the new value into the global variable
    global trackbar_value5
    trackbar_value5 = new_value
    return


cv2.namedWindow("Processed")
cv2.createTrackbar("lB", "Processed", trackbar_value, 255, updateValue)
cv2.createTrackbar("lG", "Processed", trackbar_value1, 255, updateValue1)
cv2.createTrackbar("lR", "Processed", trackbar_value2, 255, updateValue2)
cv2.createTrackbar("hB", "Processed", trackbar_value3, 255, updateValue3)
cv2.createTrackbar("hG", "Processed", trackbar_value4, 255, updateValue4)
cv2.createTrackbar("hR", "Processed", trackbar_value5, 255, updateValue5)

blobparams = cv2.SimpleBlobDetector_Params()
blobparams.filterByArea = True
blobparams.minArea = 100
blobparams.maxArea = 100000
blobparams.filterByCircularity = False
blobparams.minDistBetweenBlobs = 10
blobparams.filterByInertia = False
blobparams.filterByConvexity = False
blobparams.filterByColor = False
detector = cv2.SimpleBlobDetector_create(blobparams)

fps = 0
str_fps = " "
seconds = 0

pipeline = rs.pipeline()
config = rs.config()

# config.enable_device('801212070130')

# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

profile = pipeline.start(config)
# profile = pipeline.start()

while True:

    start = time.time()
    # read the image from the camera
    frame = pipeline.wait_for_frames()
    #   depth_frame = frame.get_depth_frame()
    print(frame.profile)
    color_frame = frame.get_color_frame()
    frame = np.asanyarray(color_frame.get_data())
    # ret, frame = cap.read()

    # You will need this later
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # colour detection limits
    lB = trackbar_value
    lG = trackbar_value1
    lR = trackbar_value2
    hB = trackbar_value3
    hG = trackbar_value4
    hR = trackbar_value5
    lowerLimits = np.array([lB, lG, lR])
    upperLimits = np.array([hB, hG, hR])

    # Our operations on the frame come here
    thresholded = cv2.inRange(hsv, lowerLimits, upperLimits)
    outimage = cv2.bitwise_and(hsv, hsv, mask=1 - thresholded)

    # Remove noise
    # kernel = np.ones((5, 5), np.uint8)
    # eroded = cv2.erode(mask, kernel)
    # dilated = cv2.dilate(mask, kernel)

    keypoints = detector.detect(thresholded)
    for keypoint in keypoints:
        x = keypoint.pt[0]
        y = keypoint.pt[1]
    frame = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.putText(frame, str_fps, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    try:
        cv2.putText(frame, '(' + str(int(round(x))) + ',' + str(int(round(y))) + ')', (int(round(x)), int(round(y))),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    except NameError:
        pass
    else:
        pass

    cv2.imshow('Original', frame)

    # cv2.imshow('Thresholded', thresholded)

    # Display the resulting frame
    cv2.imshow('Processed', thresholded)

    # Quit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    end = time.time()
    seconds += end - start
    if seconds < 1:
        fps += 1
    elif seconds >= 1:
        str_fps = str(int(round(fps)))
        seconds = 0
        fps = 0

# When everything done, release the capture
# cap.release()
cv2.destroyAllWindows()