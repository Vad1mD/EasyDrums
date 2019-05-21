# Drums class
import cv2 as cv
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


