# Stick class
import numpy as np
import math
import cv2 as cv

class Stick:

    color = ''

    def __init__(self, color):

        if color == 'red':
            self.color = 'red'
            self.hsv = np.array([[166, 84, 141], [186, 255, 255]])
            self.rgb = (0, 0, 255)

        elif color == 'blue':
            self.color = 'blue'
            self.hsv = np.array([[97, 100, 117], [117, 255, 255]])
            self.rgb = (255, 0, 0)

        self.enter_time = 0;
        self.velocity = 0
        self.last_5_centers = [(0, 0)]*5
        self.tom2_hit = False
        self.tom1_hit = False
        self.hi_hat_hit = False
        self.snare_hit = False



    def calculate_velocity(self):

        x = (self.last_5_centers[4][0] - self.last_5_centers[2][0]) ** 2
        y = (self.last_5_centers[4][1] - self.last_5_centers[4][1]) ** 2

        self.velocity = round(math.sqrt (x + y))

    def update_centers(self, center):

        self.last_5_centers.pop(0)
        self.last_5_centers.append(center)


    def determine_volume(self):

        volume = float(self.velocity / 50)
        if volume > 1.0:
            volume = 1.0

        return volume


# Drums class
class Drums:

    def __init__(self):

        # coordinates
        self.tom2_coordinates = (50, 350, 200, 450)
        self.tom1_coordinates = (430, 350, 580, 450)
        self.hi_hat_coordinates = (80, 110, 230, 210)
        self.snare_coordinates = (410, 110, 560, 210)


    def draw_drum_areas(self, mat):

        cv.rectangle(mat, (50, 350), (200, 450), (88, 138, 122), 1)
        cv.rectangle(mat, (430, 350), (580, 450), (185, 122, 53), 1)
        cv.rectangle(mat, (80, 110), (230, 210), (160, 0, 160), 1)
        cv.rectangle(mat, (410, 110), (560, 210), (100, 120, 60), 1)


    def change_drum_color(self):
        return


