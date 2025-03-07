# necessary imports
import cv2
import numpy as np
import pygame
from drum_system import app,midi_extractor,visualization
import imutils
from music21 import converter, corpus, instrument, midi, note, chord, pitch

# pygame init
pygame.mixer.pre_init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

# Music mp3 load
#pygame.mixer.music.load("add path to audio")
#pygame.mixer.music.play()
# Importing sounds

if __name__ == "__main__":
    app = app.App()
    app.run()



