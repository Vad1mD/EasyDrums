from typing import Dict, List, Tuple, Any
from music21 import midi, note, chord


class MidiExtractor:
    def __init__(self) -> None:
        self.mf: midi.MidiFile = midi.MidiFile()
        self.midi_notes: List[float] = [42.0, 38.0, 47.0, 48.0]

    def get_tabs(self, path: str) -> Dict[Any, Any]:
        # Read midi file
        self.mf.open(path)
        self.mf.read()
        self.mf.close()

        m21_stream = midi.translate.midiTracksToStreams(self.get_tracks(self.mf))

        # Extracting drum notes
        notes_offset = list(self.extract_offset(m21_stream))

        # Extracting notes that are relevant to current drum set
        existing_notes = self.get_existing_notes(notes_offset)

        notes_dict = self.list_to_dict(existing_notes)

        return notes_dict

    def get_tracks(self, midi_file: Any) -> List[Any]:
        """Extract tracks with drums in them."""
        tracks_with_drums = []
        for track in midi_file.tracks:
            if 10 in track.getChannels():
                tracks_with_drums.append(track)
        return tracks_with_drums

    def extract_offset(self, midi_part: Any) -> List[Tuple[float, Any]]:
        """Extract offsets of notes and chords."""
        offsets = []
        for nt in midi_part.flat.notes:
            if isinstance(nt, note.Note):
                offsets.append((max(0.0, nt.pitch.ps), nt.offset))
            elif isinstance(nt, chord.Chord):
                for pitch in nt.pitches:
                    offsets.append((max(0.0, pitch.ps), nt.offset))
        return offsets

    def get_existing_notes(self, notes: List[Tuple[float, Any]]) -> List[Tuple[float, Any]]:
        """Filter notes that are relevant to the current drum set."""
        return [tab for tab in notes if tab[0] in self.midi_notes]

    def list_to_dict(self, notes_list: List[Tuple[float, Any]]) -> Dict[Any, Any]:
        """Convert list of notes to a dictionary with time as keys."""
        notes_dict: Dict[Any, Any] = {}
        time_list: List[float] = []
        last_entry: Any = 0
        last_note: float = 0
        flag: bool = False

        for note, time in notes_list:
            if flag:
                time_list.append(last_note)
                notes_dict[last_entry] = None
                flag = False

            if time not in notes_dict and not time_list:
                time_list.append(note)
                notes_dict[time] = None
                last_entry = time
            elif time not in notes_dict and time_list:
                notes_dict[last_entry] = time_list.copy()
                last_entry = time
                last_note = note
                flag = True
                time_list.clear()
            else:
                time_list.append(note)

        notes_dict[last_entry] = time_list.copy()
        return notes_dict
