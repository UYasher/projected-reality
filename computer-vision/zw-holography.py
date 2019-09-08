import cv2
import numpy as np
import random
import os

# Initialize constants
width = 640
height = 360
#blank_frame = np.zeros([height, width, 4])


def getRandomImage(path):
    """
    :param path: The to randomly draw images from
    :return: a random filename, chosen among the files of the given path.
    """
    files = os.listdir(path)
    index = random.randrange(0, len(files))
    # print(index)
    # print(files[index])
    # print(path+"/"+files[index])
    return cv2.imread(path + "/" + files[index], cv2.IMREAD_UNCHANGED)


class Particle:
    """
    A particle that moves and has an image
    """

    def __init__(self, path):
        self.path = path
        self.v = np.array([0, 0])
        self.r = np.array([-1, -1])
        self.update()

    def update(self):
        self.r += self.v
        if (self.r[0] < 0) or (self.r[0] > width) or (self.r[1] < 0) or (self.r[1] > height):
            self.r = np.array([random.randint(0, width), random.randint(0, height)])
            self.v = np.array([random.randint(-30, 30), random.randint(-30, 30)])
            while np.linalg.norm(self.v) == 0:
                self.v = np.array([random.randint(-30, 30), random.randint(-30, 30)])
            self.img = getRandomImage(self.path)

    def __str__(self):
        return str(self.r) + " moving at " + str(self.v)


def zwm(directory, num_particles):
    """

    :param directory: The directory in which images are stored
    :param num_particles: The number of particles to simulate
    :return: Simulates and renders a Zach Weinersmith Holograph with the specific images and number of particles
    """

    cv2.imshow("wefwef", getRandomImage(directory))
    cv2.waitKey(50000)

    # Randomly initialize particles
    particles = [Particle(directory) for _ in range(num_particles)]

    cv2.imshow("blank", np.zeros([height, width, 4]))
    cv2.waitKey(50000)

    # Run Holograph
    while True:
        frame = np.zeros([height, width, 4])
        for p in particles:
            #print(p)
            # Update position vector
            p.update()
            # Render new frame
            #print(p.img.shape)
            # print(frame.shape)
            frame_to_add = np.zeros([height, width, 4])
            #print("p.r = " + str(p.r))
            frame_to_add[p.r[1] + max(0, -p.r[1]):p.r[1] + min(p.img.shape[0], height - p.r[1]),
            p.r[0] + max(0, -p.r[0]):p.r[0] + min(p.img.shape[1], width - p.r[0])] = \
                p.img[max(0, -p.r[1]):min(p.img.shape[0],height - p.r[1]), max(0, -p.r[0]):min(p.img.shape[1], width - p.r[0])]
            #frame = cv2.addWeighted(frame, 0.4, frame_to_add, 0.1, 0)
            frame = cv2.addWeighted(frame, 0.8, frame_to_add, 0.1, 0)
        frame = cv2.addWeighted(frame, 0.3, np.zeros([height, width, 4]), 0.7, 0)
        frame = cv2.addWeighted(frame, 0.3, np.zeros([height, width, 4]), 0.7, 0)

        # Display frame in fullscreen
        cv2.namedWindow("Zach Weinersmith Machine", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Zach Weinersmith Machine", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Zach Weinersmith Machine", frame)
        cv2.waitKey(1)

zwm("../images/rand", 10)

# TODO: Each equation should appear at most once