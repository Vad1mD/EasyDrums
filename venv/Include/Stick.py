# Stick class
import numpy as np
import math

class Stick:

    color = ''

    def __init__(self, color):

        if color == 'red':
            self.color = 'red'
            self.hsv = np.array([[160, 100, 100], [179, 255, 255]])
            self.rgb = (0, 0, 255)

        elif color == 'blue':
            self.color = 'blue'
            self.hsv = np.array([[75, 80, 100], [179, 255, 255]])
            self.rgb = (255, 0, 0)

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
