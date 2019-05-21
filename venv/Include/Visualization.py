import numpy as np
import pandas as pd
from music21 import converter, corpus, instrument, midi, note, chord, pitch
import matplotlib, scipy

midi_path = "C:/Users/dolva/PycharmProjects/EasyDrums/venv/MIDI/NothingElseMatters.mid"

# Read midi file
mf=midi.MidiFile()
mf.open(midi_path)
mf.read()
mf.close()

# Drums extraction from midi
#for i in range(len(mf.tracks)):
 #   mf.tracks[i].events = [ev for ev in mf.tracks[i].events if ev.channel == 10]

s = midi.translate.midiTrackToStream(mf.tracks[8])
print(s)
mf = midi.translate.streamToMidiFile(s)


