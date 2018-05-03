import os
from pydub import AudioSegment
import subprocess

def folderName(speechFile):
    index = -1
    while speechFile[index] != '.' and index > -len(speechFile) + 1:
        index -= 1
    return speechFile[:index]

def convert(speechFile, extension):
    """Converts speech file to the desired extension."""
    folder = folderName(speechFile)
    if not os.path.exists(folder + extension):
        #command = ['ffmpeg', "-i", speechFile, folder + extension]
        command = [
                   "ffmpeg", "-i", speechFile,
                   "-ab", "160k",
                   "-ac", "1",
                   "-vn", folder + extension
                  ]
        subprocess.call(command, shell=True)
    return folder + extension

def convertClean(speechFile, extension):
    """Uses the bril.exe file from the following URL to reduce noise: \n
        https://www.dspalgorithms.com/www/bril/bril.php"""
    folder = folderName(speechFile)
    if not os.path.exists(folder + extension):
        return None
    command = [
               'bril.exe',
               speechFile,
               folder + '-edit' + extension,
               '25'
              ]     # 25 is for generally best quality
    subprocess.call(command, shell=True)
    return folder + extension

def convertFiles(speechFile, app):
    """Only converts .wav files into .mp3 files at the moment."""
    app.updateLog('Start conversion ... ')
    folder = folderName(speechFile)
    
    sound = AudioSegment.from_wav(speechFile)
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
    app.updateLog('Finished.')
