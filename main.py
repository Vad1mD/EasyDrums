import pygame
from drum_system import app

# pygame init
pygame.mixer.pre_init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

if __name__ == "__main__":
    application: app.App = app.App()
    application.run()
