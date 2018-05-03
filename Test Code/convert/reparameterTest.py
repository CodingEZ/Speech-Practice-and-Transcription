import os
from pydub import AudioSegment

basis = AudioSegment.from_wav('Audio/basis.wav')

fileName = 'Audio/Obama-Speech.wav'
newFileName = 'Audio/Obama-Speech-1.wav'
segment = AudioSegment.from_wav(fileName)[:20000]
os.remove(fileName)
combined = basis.overlay(segment)
combined.export(newFileName, 'wav')
