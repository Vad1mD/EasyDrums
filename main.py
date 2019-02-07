# necessary imports
import cv2 as cv
import numpy as np
import pygame
import imutils

# pygame init
pygame.mixer.pre_init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

# Importing sounds

snare = pygame.mixer.Sound("venv/Sounds/snare.wav")
tom1 = pygame.mixer.Sound("venv/Sounds/tom1.wav")
tom2 = pygame.mixer.Sound("venv/Sounds/tom2.wav")
hihat = pygame.mixer.Sound("venv/Sounds/hihat.wav")

# TODO change coordinates into np array
# coordinates
tom2_coordinates = (50, 350, 200, 450)
tom1_coordinates = (430, 350, 580, 450)
hi_hat_coordinates = (80, 110, 230, 210)
snare_coordinates = (410, 110, 560, 210)

# TODO change from global to local
# global vars for hit detection
tom2_hit = False
tom1_hit = False
hi_hat_hit = False
snare_hit = False

# second lower & higher bound
lower_red = np.array([160, 100, 100])
upper_red = np.array([179, 255, 255])

# TODO - find fucking brighter balls!!!
lower_blue = np.array([75, 80, 100])
upper_blue = np.array([179, 255, 255])


def draw_drum_areas(mat):
    cv.rectangle(mat, (50, 350), (200, 450), (88, 138, 122), 2)
    cv.rectangle(mat, (430, 350), (580, 450), (185, 122, 53), 2)
    cv.rectangle(mat, (80, 110), (230, 210), (160, 0, 160), 2)
    cv.rectangle(mat, (410, 110), (560, 210), (100, 120, 60), 2)
    return


def recognize_ball(ball_center):

    global hi_hat_hit, tom1_hit, tom2_hit, snare_hit

    if 80 <= ball_center[0] <= 230 and 110 <= ball_center[1] <= 210:
        if not hi_hat_hit:
            hihat.play()
            hi_hat_hit = True
    else:
        hi_hat_hit = False

    if 430 <= ball_center[0] <= 580 and 350 <= ball_center[1] <= 450:
        if not tom1_hit:
            tom1.play()
            tom1_hit = True
    else:
        tom1_hit = False

    if 50 <= ball_center[0] <= 200 and 350 <= ball_center[1] <= 450:
        if not tom2_hit:
            tom2.play()
            tom2_hit = True

    else:
        tom2_hit = False

    if 410 <= ball_center[0] <= 560 and 110 <= ball_center[1] <= 210:
        if not snare_hit:
            snare.play()
            snare_hit = True

    else:
        snare_hit = False


# TODO determine volume
def calculate_hit_speed():
    return


# contours detection
def process_frame(mat):

    # global color ranges
    global lower_red, upper_red, lower_blue, upper_blue

    # blurring to remove noise and converting to HSV
    blur = cv.GaussianBlur(mat, (11, 11), 0)
    hsv_colors = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

    # finding contours
    find_contour(hsv_colors, lower_red, upper_red)
    find_contour(hsv_colors, lower_blue, upper_blue)

    return


# contour detection function
def find_contour(hsv, color_lower, color_upper):

    # remove small blobs in the mask
    mask = cv.inRange(hsv, color_lower, color_upper)

    # smoothen and removing leftover blobs
    mask = cv.erode(mask, None, iterations=4)
    mask = cv.dilate(mask, None, iterations=4)

    # find contours from the mask
    contour = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contour = imutils.grab_contours(contour)

    # only proceed if at least one contour was found
    if len(contour) > 0:
        # find the largest contour and compute minimum enclosing circle
        c = max(contour, key=cv.contourArea)
        ((x, y), radius) = cv.minEnclosingCircle(c)
        M = cv.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # proceed only at minimum size
        if radius > 10:
            recognize_ball(center)
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
            cv.circle(frame, center, 5, (0, 0, 255), -1)

    return


if __name__ == "__main__":

    # initiate web cam object
    cap = cv.VideoCapture(0)

    # get frames until 'q' is pressed
    while True:

        # get frame
        _, frame = cap.read()

        # TODO change to checking if the camera opened

        frame = cv.flip(frame, 1)
        # TODO - draw rectangles at the end of the process
        # drawing the drum set on the screen
        draw_drum_areas(frame)

        # resizing the window, blurring it and converting to HSV
        frame = imutils.resize(frame, width=640, height=480)

        process_frame(frame)

        # show the frame to our screen
        cv.imshow("frame", frame)
        key = cv.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

    cap.release()

    # close all windows
    cv.destroyAllWindows()
