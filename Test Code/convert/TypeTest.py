import wave
from pydub import AudioSegment

def convertParameters(file, basis='Audio/output.wav')
    recordedFile = wave.open(basis, 'rb')

    oldFile = wave.open(file, 'rb')
    sound = AudioSegment.from_wav(file)
    length = sound.duration_seconds
    numFrames = int(length * oldFile.getframerate())
    frames = oldFile.readframes(numFrames)
    oldFile.close()

    newFile = wave.open(file, 'wb')
    newFile.setparams(recordedFile.getparams())
    newFile.writeframes(frames)
    newFile.close()
