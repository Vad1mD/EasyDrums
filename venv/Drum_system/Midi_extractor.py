import numpy as np
import pandas as pd
from music21 import stream, corpus, instrument, midi, note, chord, pitch

#TODO add path getter via GUI

midi_path = "C:/Users/dolva/PycharmProjects/EasyDrums/venv/MIDI/SevenNationArmy.mid"

# Read midi file
mf=midi.MidiFile()
mf.open(midi_path)
mf.read()
mf.close()

s1 = midi.translate.midiFileToStream(mf)

# Extracting the tracks with drums in them
tracks_with_drums = []
for track in mf.tracks:
    channels_in_track = track.getChannels()
    if 10 in channels_in_track:
        tracks_with_drums.append(track)

#for i in range(len(mf.tracks)):
#            mf.tracks[i].events = [ev for ev in mf.tracks[i].events if ev.channel == 10]
s = midi.translate.midiTracksToStreams(tracks_with_drums)

def extract(midi_part):
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

