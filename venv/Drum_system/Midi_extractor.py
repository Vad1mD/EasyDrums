from music21 import midi, note, chord


class Midi_extractor:

    def __init__(self):
        self.mf=midi.MidiFile()


    def get_tabs(self, path):
        midi_path= path

        # Read midi file
        self.mf.open(midi_path)
        self.mf.read()
        self.mf.close()

        self.midi_notes = [42.0,38.0,47.0,48.0]

        m21_Stream = midi.translate.midiTracksToStreams(self.get_tracks(self.mf))

        # Extracting drum notes
        notes_offset = list(self.extract_offset(m21_Stream))

        # Extracting notes that are relevent to current drum set
        existing_notes = self.get_existing_notes(notes_offset)

        dict = self.list_to_dict(existing_notes)

        return dict


    # Extracting the tracks with drums in them
    def get_tracks(self,midi_file):

        tracks_with_drums = []

        for track in self.mf.tracks:
            channels_in_track = track.getChannels()
            if 10 in channels_in_track:
                tracks_with_drums.append(track)

        return tracks_with_drums


    def extract_offset(self,midi_part):
        parent_element=[]
        offset = []
        ret=[]
        for nt in midi_part.flat.notes:
            if isinstance(nt, note.Note):
                ret.append(max(0.0, nt.pitch.ps))
                parent_element.append(nt)
            elif isinstance(nt, chord.Chord):
                for pitch in nt.pitches:
                    ret.append(max(0.0, pitch.ps))
                    parent_element.append(nt)

        x = [n.offset for n in parent_element]

        note_offset = zip(ret,x)

        return note_offset


    def get_existing_notes(self, notes):
        l = []
        for tab in notes:
            if tab[0] in self.midi_notes:
                l.append(tab)
        return l


    def list_to_dict(self, notes_list):

        flag = False
        dict = {}
        time_list = []
        last_entry = 0
        last_note = 0

        for note,time in notes_list:

            # if encountered new time stamp
            if flag == True:
                time_list.append(last_note)
                dict[last_entry] = None
                flag = False

            if time not in dict.keys() and len(time_list)==0:
                time_list.append(note)
                dict[time]=None
                last_entry = time

            elif time not in dict.keys() and len(time_list)>0 :
                dict[last_entry] = time_list.copy()
                last_entry = time
                last_note = note
                flag = True
                time_list.clear()

            else:
                 time_list.append(note)

        # Adding last element
        dict[last_entry] = time_list.copy()

        return dict

