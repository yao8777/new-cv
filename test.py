import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)  # 使用 GPIO 11 控制電燈

try:
    while True:
        GPIO.output(11, GPIO.HIGH)  # 打開電燈
        time.sleep(1)
        GPIO.output(11, GPIO.LOW)   # 關閉電燈
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()