import cv2
import RPi.GPIO as GPIO
import time

# 設定 GPIO 引腳
LED_PIN = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# 初始化相機
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# 初始化背景差異檢測器
fgbg = cv2.createBackgroundSubtractorMOG2()

# 設定計時器
timer_start = None

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)
    fgmask = cv2.erode(fgmask, None, iterations=2)
    fgmask = cv2.dilate(fgmask, None, iterations=2)

    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 檢測到移動時控制電燈開啟並框選移動物體
    if len(contours) > 0:
        GPIO.output(LED_PIN, GPIO.HIGH)

        # 重置計時器
        timer_start = time.time()

        for contour in contours:
            # 忽略小區域
            if cv2.contourArea(contour) < 1000:
                continue

            # 計算並繪製矩形框
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    else:
        # 如果計時器存在且超過30秒，則關閉LED
        if timer_start is not None and time.time() - timer_start > 30:
            GPIO.output(LED_PIN, GPIO.LOW)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# 釋放相機資源、關閉視窗並釋放 GPIO 資源
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()