import cv2
import numpy as np

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('/home/shriyash/Downloads/640x360_360p.mp4')

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")

# Read until video is completed
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        # Display the resulting frame
        cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        height, width, channels = frame.shape

        top_offset = 3
        thickness = -1
        color = (0,255,0)
        r = 50

        frame = cv2.rectangle(frame, (0, 0), (r, r), color, thickness)
        frame = cv2.rectangle(frame, (0, height), (r, height-r), color, thickness)
        frame = cv2.rectangle(frame, (width, height), (width-r, height-r), color, thickness)
        frame = cv2.rectangle(frame, (width, 0), (width - r, r), color, thickness)

        '''
        # Top Right Frame - Green
        frame = cv2.line(frame, (width, 10), (width, 100), (0, 255, 0), thickness)
        frame = cv2.line(frame, (width-10, top_offset), (width-100, top_offset), (0, 255, 0), thickness)

        # Bottom Right Frame - Red
        frame = cv2.line(frame, (width, height-10), (width, height-100), (0, 0, 255), thickness)
        frame = cv2.line(frame, (width-10, height), (width-100, height), (0, 0, 255), thickness)

        # Bottom Left Frame - Yellow
        frame = cv2.line(frame, (0, height-10), (0, height-100), (0, 255, 255), thickness)
        frame = cv2.line(frame, (10, height), (100, height), (0, 255, 255), thickness)
        '''

        cv2.imshow("Frame", frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()