import cv2 as cv
from Drum_system import Midi_extractor
import random

class Visualization:

    def __init__(self):
        self.midi_path = "C:/Users/dolva/PycharmProjects/EasyDrums/venv/MIDI/SevenNationArmy.mid"
        self.midi = Midi_extractor.Midi_extractor()
        self.tabs = self.midi.get_tabs(self.midi_path)

    def get_tabs(self):
        return self.tabs



class note_box:

    def __init__(self, curr_note):
        self.delta = 0
        self.done = False
        self.notes = [38,42,47,48]
        self.curr_note = curr_note

    def show(self,frame):
        if self.delta < 380:
            for note in self.curr_note:
                if note == 38:
                    cv.rectangle(frame, (50, self.delta), (200, self.delta + 100), (0, 255, 0), 1)
                elif note == 42:
                    cv.rectangle(frame, (430, self.delta), (580, self.delta + 100), (0, 255, 0), 1)
                elif note == 47:
                    cv.rectangle(frame, (80, self.delta), (230, self.delta + 100), (255, 0, 0), 1)
                elif note == 48:
                    cv.rectangle(frame, (410, self.delta), (560, self.delta + 100), (255, 0, 0), 1)

                self.delta = self.delta + 5
        else:
            self.done = True

    def get_done(self):
        return self.done
