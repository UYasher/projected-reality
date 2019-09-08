import urllib.request
import cv2
import numpy as np
import time



def average_border(img, f=False):

    height, width, channels = img.shape

    prev_mask = np.zeros(img.shape[:2], dtype="uint8")
    for bw in range(1, int(height/2)):
        mask = np.ones(img.shape[:2], dtype="uint8")
        cv2.rectangle(mask, (bw, bw), (img.shape[1] - bw, img.shape[0] - bw), 0, -1)
        current_mask = cv2.bitwise_xor(mask, prev_mask)

        output = cv2.bitwise_and(img, img, mask=current_mask)
        cv2.imshow('out', output)
        cv2.waitKey(500000)

        cummulative_mean = cv2.mean(img, mask=mask)
        current_mean = cv2.mean(img, mask=current_mask)
        print("cummulative @ " + str(bw) + ": " + str(cummulative_mean))
        print("current @ " + str(bw) + ": " + str(current_mean))
        print("")
        prev_mask = mask

    #output = cv2.bitwise_and(img, img, mask=mask)
    output = cv2.bitwise_and(img, img, mask=current_mask)
    cv2.imshow('out', output)
    cv2.waitKey(5000)


def get_angles(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    cv2.imshow('hsvimg', hsv_img)

    color_range = {
        "red": [(100, 80, 180), (140, 128, 255)], # Noisy, params may need adjustment (too sensitive)
        "green": [(40, 40, 190), (80, 128, 255)],
        "blue": [(140, 100, 0), (180, 255, 255)],
    }

    red_mask = cv2.inRange(hsv_img, color_range["green"][0], color_range["green"][1])
    red_filter = cv2.bitwise_and(img, img, mask=red_mask)
    cv2.imshow('red_mask', red_filter)

    kernel = np.ones((4, 4), np.uint8)
    erosion = cv2.erode(red_mask, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

    cv2.imshow('cnt', cnt)

    for c in contours:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        print("("+str(cX)+", "+str(cY)+")")

#URL = "http://192.168.43.1:8080/shot.jpg"
URL = "http://10.251.83.80:8080/shot.jpg"

while True:
    print("just entered loop")
    img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
    print("just got image")
    img = cv2.imdecode(img_arr, -1)
    print("just encoded image")
    cv2.imshow('IPWebcam', img)
    print("just displayed image")
    get_angles(img)
    #average_border(img)

    if cv2.waitKey(10):
        print("waitKey triggered")