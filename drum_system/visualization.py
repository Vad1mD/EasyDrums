import cv2 as cv
from drum_system import midi_extractor
import os


class Visualization:
    def __init__(self):
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.midi_path = os.path.join(root_dir, "data/midi/SevenNationArmy.mid")
        self.midi = midi_extractor.MidiExtractor()
        self.tabs = self.midi.get_tabs(self.midi_path)

    def get_tabs(self) -> dict:
        """Get the tabs from the MIDI extractor."""
        return self.tabs


class NoteBox:
    def __init__(self, curr_note: list):
        self.delta = 0
        self.done = False
        self.notes = [38, 42, 47, 48]
        self.curr_note = curr_note

    def show(self, frame) -> None:
        """Show the note box on the given frame."""
        if self.delta < 380:
            for note in self.curr_note:
                if note == 38:
                    cv.rectangle(
                        frame, (50, self.delta), (200, self.delta + 100), (0, 255, 0), 1
                    )
                elif note == 42:
                    cv.rectangle(
                        frame,
                        (430, self.delta),
                        (580, self.delta + 100),
                        (0, 255, 0),
                        1,
                    )
                elif note == 47:
                    cv.rectangle(
                        frame, (80, self.delta), (230, self.delta + 100), (255, 0, 0), 1
                    )
                elif note == 48:
                    cv.rectangle(
                        frame,
                        (410, self.delta),
                        (560, self.delta + 100),
                        (255, 0, 0),
                        1,
                    )
            self.delta += 5
        else:
            self.done = True

    def get_done(self) -> bool:
        """Check if the note box is done."""
        return self.done
