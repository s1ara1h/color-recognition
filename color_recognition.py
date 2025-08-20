# -*- coding: utf-8 -*-
# Phone camera via Wi-Fi (DroidCam) + center color name

import cv2
import numpy as np

IP = "192.168.xxx.xxx"
PORT = 4747
PATH = "video" 

url = f"http://{IP}:{PORT}/{PATH}"
cap = cv2.VideoCapture(url)
if not cap.isOpened():
    raise RuntimeError(f"Could not open Wi-Fi stream: {url}")

COLOR_RANGES = {
    "Red1":  ((0,   120, 70),  (10,  255, 255)),
    "Red2":  ((170, 120, 70),  (180, 255, 255)),
    "Green": ((35,  80,  70),  (85,  255, 255)),
    "Blue":  ((90,  80,  70),  (130, 255, 255)),
    "Yellow":((20,  80,  70),  (35,  255, 255)),
    "Orange":((10,  80,  70),  (20,  255, 255)),
    "Purple":((130, 80,  70),  (160, 255, 255)),
    "White": ((0,   0,   200), (180, 40,  255)),
    "Black": ((0,   0,   0),   (180, 255, 40)),
}

def classify_color(hsv_pixel):
    h, s, v = map(int, hsv_pixel)
    if ((0 <= h <= 10) and (120 <= s <= 255) and (70 <= v <= 255)) or \
       ((170 <= h <= 180) and (120 <= s <= 255) and (70 <= v <= 255)):
        return "Red"
    for name in ["Green","Blue","Yellow","Orange","Purple","White","Black"]:
        lo, hi = COLOR_RANGES[name]
        if lo[0] <= h <= hi[0] and lo[1] <= s <= hi[1] and lo[2] <= v <= hi[2]:
            return name
    return "No Recognition"

while True:
    ok, frame = cap.read()
    if not ok or frame is None or frame.size == 0:
        break

    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2

    b, g, r = [int(x) for x in frame[cy, cx]]
    print([b, g, r])

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color_name = classify_color(hsv[cy, cx])

    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
    cv2.putText(frame, color_name, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.6,
                (0, 255, 0), 3, cv2.LINE_AA)
    cv2.rectangle(frame, (cx-20, cy-20), (cx+20, cy+20), (0, 255, 255), 1)

    cv2.imshow("Phone Cam (Wi-Fi)", frame)
    if cv2.waitKey(1) & 0xFF in (27, ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
