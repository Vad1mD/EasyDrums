from typing import Dict, List, Any
import cv2 as cv
from drum_system import midi_extractor
import os
import numpy as np


class Visualization:
    def __init__(self) -> None:
        root_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.midi_path: str = os.path.join(root_dir, "data/midi/SevenNationArmy.mid")
        self.midi: midi_extractor.MidiExtractor = midi_extractor.MidiExtractor()
        self.tabs: Dict[Any, Any] = self.midi.get_tabs(self.midi_path)

    def get_tabs(self) -> Dict[Any, Any]:
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


def note_box(curr_note: List[float]) -> NoteBox:
    """Factory function to create a NoteBox instance."""
    return NoteBox(curr_note)
