import os
import io
from pydub import AudioSegment
import pyaudio
import wave

spliceLength = 60
patchLength = 8000

def filterName(speech_file):
    if not isFile(speech_file):
        return None
    newName = speech_file.replace(" ", "-")
    index = extensionIndex(newName)
    if newName != speech_file:
        os.rename(speech_file, newName)
    if newName[index:] != '.wav':       # check if it is a .wav file
        print('Had to convert file from', newName[index:], 'to .wav. Now referring to .wav file')
        convert(newName, '.wav')
        newName = newName[:index] + '.wav'
    return newName

def isFile(speech_file):
    if not os.path.isfile(speech_file):
        print('Not a file! Please input a file')
        return False
    return True

def extensionIndex(speech_file):
    index = -1
    while speech_file[index] != '.' and index > -len(speech_file) + 1:
        index -= 1
    return index

def mkFilesLocation(speech_file):
    index = extensionIndex(speech_file)
    folder = speech_file[:index]
    if not os.path.exists(folder):
        print('Made new directory.')
        os.mkdir(folder)

def divideFiles(speech_file):
    '''Only divides .wav files at the moment.'''
    print('Start division ... ', end='')
    index = extensionIndex(speech_file)
    folder = speech_file[:index]

    sound = AudioSegment.from_wav(speech_file)
    length = sound.duration_seconds
    for i in range(int(length//spliceLength)):
        try:    newSound = sound[i*spliceLength*1000 : (i+1)*spliceLength*1000]
        except: newSound = sound[i*spliceLength*1000 : ]
        newSound.export(folder + '/splice.' + str(i) + '.wav', format='wav')
        try:    newSound = sound[(i+1)*spliceLength*1000 - patchLength//2 : \
                                 (i+1)*spliceLength*1000 + patchLength//2]
        except: newSound = sound[(i+1)*spliceLength*1000 - patchLength//2 : ]
        newSound.export(folder + '/patch.' + str(i) + '.wav', format='wav')
        try:    newSound = sound[(i+1)*spliceLength*1000 - patchLength//4 : \
                                 (i+1)*spliceLength*1000 + patchLength//4]
        except: newSound = sound[(i+1)*spliceLength*1000 - patchLength//4 : ]
        newSound.export(folder + '/insidepatch.' + str(i) + '.wav', format='wav')
    print('Finished.')

def reparameterFiles(speech_file):
    print('Start reparameterizaion ... ', end='')
    index = extensionIndex(speech_file)
    folder = speech_file[:index]
    
    sound = AudioSegment.from_wav(speech_file)
    length = sound.duration_seconds
    basis = AudioSegment.from_wav('Audio/basis.wav')
    basis = basis[:spliceLength*1000] - 100       # reduce volume of basis by 100 decibels
    for i in range(int(length//spliceLength)):
        fileName = folder + '/splice.' + str(i) + '.wav'
        if os.path.exists(fileName):
            segment = AudioSegment.from_wav(fileName)
            os.remove(fileName)
            combined = basis.overlay(segment)
            combined.export(fileName, 'wav')
        fileName = folder + '/patch.' + str(i) + '.wav'
        if os.path.exists(fileName):
            segment = AudioSegment.from_wav(fileName)
            os.remove(fileName)
            combined = basis[:patchLength].overlay(segment)
            combined.export(fileName, 'wav')
        fileName = folder + '/insidepatch.' + str(i) + '.wav'
        if os.path.exists(fileName):
            segment = AudioSegment.from_wav(fileName)
            os.remove(fileName)
            combined = basis[:patchLength//2].overlay(segment)
            combined.export(fileName, 'wav')
    print('Finished.')

def convert(speech_file, extension):
    import subprocess
    index = extensionIndex(speech_file)
    if not os.path.exists(speech_file[:index] + extension):
        #command = ['ffmpeg', "-i", speech_file, speech_file[:index] + extension]
        command = [
                   "ffmpeg", "-i", speech_file,
                   "-ab", "160k",
                   "-ac", "1",
                   "-vn", speech_file[:index] + extension
                  ]
        subprocess.call(command, shell=True)

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

def removeFiles(speech_file):
    '''Only removes .wav files at the moment.'''
    print('Start removal ... ', end='')
    index = extensionIndex(speech_file)
    folder = speech_file[:index]
    
    sound = AudioSegment.from_wav(speech_file)
    length = sound.duration_seconds
    for i in range(int(length//spliceLength)):
        fileName = folder + '/splice.' + str(i) + '.wav'
        if os.path.exists(fileName):
            os.remove(fileName)
        fileName = folder + '/patch.' + str(i) + '.wav'
        if os.path.exists(fileName):
            os.remove(fileName)
        fileName = folder + '/insidepatch.' + str(i) + '.wav'
        if os.path.exists(fileName):
            os.remove(fileName)
    print('Finished.')

def transcribeFiles(speech_file, extension):
    print('Starting transcription ... ')
    index = extensionIndex(speech_file)
    folder = speech_file[:index]

    if not os.path.exists(folder):
        print('File does not exist, cannot call transcription')
        return

    sound = AudioSegment.from_wav(speech_file)
    length = sound.duration_seconds
    for i in range(int(length//spliceLength)):
        fileName = folder + '/splice.' + str(i) + extension
        if os.path.exists(fileName):
            transcribeOne(fileName)
        fileName = folder + '/patch.' + str(i) + extension
        if os.path.exists(fileName):
            transcribeOne(fileName)
        fileName = folder + '/insidepatch.' + str(i) + extension
        if os.path.exists(fileName):
            transcribeOne(fileName)
    print('Finished.')

#############################################################################
# This code is straight from the google speech recognition documentation
'https://cloud.google.com/speech-to-text/docs/sync-recognize'
#############################################################################

def transcribeOne(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=speech.Encoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US')

    transcript = ""
    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        #print('Transcript: {}'.format(result.alternatives[0].transcript))
        transcript += result.alternatives[0].transcript
    print(transcript)
    print()

# sets up credentials to allow someone who holds the required json file to
# use speech recognition
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Youtube Transcript Translator-1afc5757090d.json"


file = 'Audio/Obama-Speech.mp3'
file = filterName(file)
mkFilesLocation(file)
divideFiles(file)
reparameterFiles(file)
transcribeFiles(file, '.wav')

