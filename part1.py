import cv2 as cv
import numpy as np

minH = 0
minS = 0
minV = 0
maxH = 180
maxS = 255
maxV = 255

kernel = np.ones((3, 3), np.uint8)


def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print("H:", hsv[y, x, 0], "   S:", hsv[y, x, 1], "  V:", hsv[y, x, 2])
        # print("B:", bgr[y, x, 0], "   G:", bgr[y, x, 1], "  R:", bgr[y, x, 2])


cap = cv.VideoCapture(0)
cv.namedWindow("Video", cv.WINDOW_KEEPRATIO)
cv.resizeWindow("Video", 960, 540)
cv.namedWindow("Tracker", cv.WINDOW_KEEPRATIO)
cv.resizeWindow("Tracker", 960, 540)


def setMinH(h):
    global minH
    minH = h


def setMaxH(h):
    global maxH
    maxH = h


def setMinS(s):
    global minS
    minS = s


def setMaxS(s):
    global maxS
    maxS = s


def setMinV(v):
    global minV
    minV = v


def setMaxV(v):
    global maxV
    maxV = v


cv.createTrackbar("minH", "Video", 0, 180, setMinH)
cv.createTrackbar("minS", "Video", 0, 255, setMinS)
cv.createTrackbar("minV", "Video", 0, 255, setMinV)
cv.createTrackbar("maxH", "Video", 0, 180, setMaxH)
cv.createTrackbar("maxS", "Video", 0, 255, setMaxS)
cv.createTrackbar("maxV", "Video", 0, 255, setMaxV)

cv.setMouseCallback("Video", onMouse, 0)

while True:
    status, bgr = cap.read()

    # Convert from BGR to HSV
    hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)

    threshold = cv.inRange(hsv, (minH, minS, minV), (maxH, maxS, maxV))

    cv.imshow("Video", bgr)

    threshold = cv.dilate(threshold, kernel)
    threshold = cv.erode(threshold, kernel)
    # threshold = cv.morphologyEx(threshold, cv.MORPH_CLOSE, kernel)
    cv.imshow("Tracker", threshold)

    k = cv.waitKey(1)
    if k == 27:
        break
cv.destroyAllWindows()
