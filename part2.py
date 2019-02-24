import cv2 as cv
import numpy as np

cap = image1 = cv.VideoCapture(0)
status, img = cap.read()

average = np.float32(img)

cv.namedWindow("Video", cv.WINDOW_KEEPRATIO)

while True:
    status, img = cap.read()
    blur = cv.GaussianBlur(img, (21, 21), 0)
    cv.accumulateWeighted(blur, average, 0.2)
    res = cv.convertScaleAbs(average)
    diff = cv.absdiff(res, img)
    gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    threshold = cv.inRange(gray, 10, 255)
    blur = cv.GaussianBlur(threshold, (21, 21), 0)
    threshold = cv.inRange(blur, 200, 255)

    # Find the contours
    contours, hierarchy = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # cv.drawContours(img, contours, -1, (0, 255, 0), 3)

    # Draw the rectangles around the movement
    for c in contours:
        if cv.contourArea(c) > 7500:
            (x, y, w, h) = cv.boundingRect(c)
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv.imshow("Video", img)

    k = cv.waitKey(1)
    if k == 27:
        break
cv.destroyAllWindows()
