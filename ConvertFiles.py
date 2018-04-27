def convertFiles(speech_file):
    '''Only converts .wav files into .mp3 files at the moment.'''
    print('Start conversion ... ', end='')
    index = extensionIndex(speech_file)
    folder = speech_file[:index]
    
    sound = AudioSegment.from_wav(speech_file)
    length = sound.duration_seconds
    for i in range(int(length//spliceLength)):
        fileName = folder + '/splice.' + str(i) + '.wav'
        if os.path.exists(fileName):
            convert(fileName, '.mp3')
        fileName = folder + '/patch.' + str(i) + '.wav'
        if os.path.exists(fileName):
            convert(fileName, '.mp3')
        fileName = folder + '/insidepatch.' + str(i) + '.wav'
        if os.path.exists(fileName):
            convert(fileName, '.mp3')
    print('Finished.')
