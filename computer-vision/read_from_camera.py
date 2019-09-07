import urllib.request
import cv2
import numpy as np
import time


def get_angles(img):
    #hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    #cv2.imshow('hsvimg', hsv_img)
    red_mask = cv2.inRange(img, (0, 0, 150), (20, 20, 255))
    cv2.imshow('red_mask', red_mask)


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
    get_angles(img)

    if cv2.waitKey(10):
        print("waitKey triggered")