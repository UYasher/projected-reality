import cv2
import numpy as np
import random
import os

# Initialize constants
width = 640
height = 360
blank_frame = np.zeroes(width, height)


def getRandomImage(path):
    """
    :param path: The to randomly draw images from
    :return: a random filename, chosen among the files of the given path.
    """
    files = os.listdir(path)
    index = random.randrange(0, len(files))
    return cv2.imread(files[index], cv2.IMREAD_UNCHANGED)


class Particle:
    """
    A particle that moves and has an image
    """
    def __init__(self, img):
        self.img = img
        self.v = np.zeros([2])
        self.r = np.array([-1, -1])
        self.update()

    def update(self):
        self.r += self.v
        if (self.r[0] < 0) or (self.r[0] > width) or (self.r[1] < 0) or (self.r[1] > height):
            self.r = np.array([random.randint(width), random.randint(height)])
            self.v = np.array([random.randint(10, 30)], random.randint(10, 100))


def zwm(directory, num_particles):
    """

    :param directory: The directory in which images are stored
    :param num_particles: The number of particles to simulate
    :return: Simulates and renders a Zach Weinersmith Holograph with the specific images and number of particles
    """

    # Randomly initialize particles
    particles = [
        Particle(getRandomImage(directory)) in range(num_particles)
    ]

    # Run Holograph
    while True:
        frame = blank_frame()
        for p in particles:
            # Update position vector
            p.update()
            # Render new frame
            frame = cv2.addWeighted(frame, 0.4, p.img, 0.1, 0)

        # Display frame in fullscreen
        cv2.namedWindow("Zach Weinersmith Machine", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Zach Weinersmith Machine", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Zach Weinersmith Machine", frame)
