# necessary imports
import cv2 as cv
import numpy as np
import pygame
from Drum_system import App
import imutils
from Include.Stick import Stick
from Include.Drums import Drums
from music21 import converter, corpus, instrument, midi, note, chord, pitch

# pygame init
pygame.mixer.pre_init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

# Importing sounds

snare = pygame.mixer.Sound("venv/Sounds/snare.wav")
tom1 = pygame.mixer.Sound("venv/Sounds/tom1.wav")
tom2 = pygame.mixer.Sound("venv/Sounds/tom2.wav")
hihat = pygame.mixer.Sound("venv/Sounds/hihat.wav")


if __name__ == "__main__":
    #app = App.App()
    #app.run()



