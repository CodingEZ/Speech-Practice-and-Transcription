def convertParameters(file, basis='Audio/basis.wav'):
    '''Contains some kind of error that prevents transcription.'''
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
    print('Converted Parameters.')
