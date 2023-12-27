import cv2
import numpy as np
import os

cap= cv2.VideoCapture (1)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

area = width * height

ret, frame = cap.read()
avg = cv2.blur (frame, (4, 4))
avg_float = np.float32(avg)

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break

    blur= cv2.blur (frame, (4, 4))
    diff= cv2.absdiff(avg, blur)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2. threshold (gray, 25, 255, cv2.THRESH_BINARY)

    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    (cnts, _) = cv2.findContours (thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    hasMotion=False

    for c in cnts:
        if cv2.contourArea (c) < 2500:
            continue

        hasMotion = True

        (x, y, w, h) = cv2.boundingRect(c)

        cv2.rectangle(frame, (x, y), (x+w, y + h), (0, 255, 0), 2)

    cv2.accumulateWeighted(blur, avg_float, 0.01)
    avg = cv2.convertScaleAbs (avg_float)
    cv2.imshow("test", frame)
    key= cv2.waitKey(1)

    if key == ord('q'):
        break

cap.release()