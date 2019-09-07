import urllib.request
import cv2
import numpy as np
import time

URL = "http://192.168.43.1:8080/shot.jpg"
while True:
    print("just entered loop")
    img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
    print("just got image")
    img = cv2.imdecode(img_arr, -1)
    print("just encoded image")
    cv2.namedWindow("IPWebcam", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("IPWebcam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('IPWebcam', img)
    print("just displayed image")

    if cv2.waitKey(10):
        print("waitKey triggered")
