# import the necessary packages
import numpy as np
import imutils
import cv2
from drum_system import tools,visualization
import pygame
import time

class App:

    def __init__(self):

        self.red_stick = tools.Stick('red')
        self.blue_stick = tools.Stick('blue')
        self.sticks = [self.red_stick, self.blue_stick]

        self.drums = tools.Drums()

        pygame.mixer.pre_init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

        # Importing sounds

        self.snare = pygame.mixer.Sound("venv/Sounds/snare.wav")
        self.tom1 = pygame.mixer.Sound("venv/Sounds/tom1.wav")
        self.tom2 = pygame.mixer.Sound("venv/Sounds/tom2.wav")
        self.hihat = pygame.mixer.Sound("venv/Sounds/hihat.wav")

    def run(self):
        vs = visualization.Visualization()
        tabs = vs.get_tabs()
        camera = cv2.VideoCapture(0)
        start = time.time()
        nb = []
        offsets_done = []

        while True:
            # grab the current frame and flip it
            ret, frame = camera.read()
            finish = time.time()
            frame_time = round((finish - start),1)

            frame = cv2.flip(frame, 1)

            # resize the frame
            frame = imutils.resize(frame, width=640, height=480)

            self.drums.draw_drum_areas(frame)

            last_time = 0
            if frame_time in tabs.keys():
                if frame_time in offsets_done:
                    pass
                else:
                    offsets_done.append(frame_time)
                    nb.append(visualization.note_box(tabs.get(frame_time)))

            if nb:
                for item in nb:
                    item.show(frame)
                    if item.get_done():
                        nb.remove(item)

            self.process_frame(frame)


            # show the frame to our screen
            cv2.imshow("Frame", frame)

            key = cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break

            # cleanup the camera and close any open windows
        camera.release()
        cv2.destroyAllWindows()


    def process_frame(self, single_frame):

        blurred = cv2.GaussianBlur(single_frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # for each color in dictionary check object in frame
        for stick in self.sticks:
            # construct a mask for the color from dictionary`1, then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            kernel = np.ones((11, 11), np.uint8)
            mask = cv2.inRange(hsv, stick.hsv[0], stick.hsv[1])
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                stick.update_centers(center)
                stick.calculate_velocity()
                # only proceed if the radius meets a minimum size. Correct this value for your obect's size
                if radius > 0.5:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    self.recognize_ball(center, stick)
                    cv2.circle(single_frame, (int(x), int(y)), int(radius), stick.rgb, 2)


    def recognize_ball(self, ball_center, drum_stick):
        volume = drum_stick.determine_volume()
        if 80 <= ball_center[0] <= 230 and 110 <= ball_center[1] <= 210:
            if not drum_stick.hi_hat_hit:
                #volume = drum_stick.determine_volume()
                self.hihat.set_volume(volume)
                self.hihat.play()
                drum_stick.hi_hat_hit = True
        else:
            drum_stick.hi_hat_hit = False

        if 430 <= ball_center[0] <= 580 and 350 <= ball_center[1] <= 450:
            if not drum_stick.tom1_hit:
                #volume = drum_stick.determine_volume()
                self.tom1.set_volume(volume)
                self.tom1.play()
                drum_stick.tom1_hit = True
        else:
            drum_stick.tom1_hit = False

        if 50 <= ball_center[0] <= 200 and 350 <= ball_center[1] <= 450:
            if not drum_stick.tom2_hit:
                #volume = drum_stick.determine_volume()
                self.tom2.set_volume(volume)
                self.tom2.play()
                drum_stick.tom2_hit = True

        else:
            drum_stick.tom2_hit = False

        if 410 <= ball_center[0] <= 560 and 110 <= ball_center[1] <= 210:
            if not drum_stick.snare_hit:
                #volume = drum_stick.determine_volume()
                self.snare.set_volume(volume)
                self.snare.play()
                drum_stick.snare_hit = True

        else:
            drum_stick.snare_hit = False

