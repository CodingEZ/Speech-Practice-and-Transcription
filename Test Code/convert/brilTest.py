import subprocess
import os

def filterName(speechFile):
    print('Filtering name: ' + speechFile + ' ... ')
    newName = speechFile.replace(" ", "-")
    index = extensionIndex(newName)

    if newName != speechFile:
        os.rename(speechFile, newName)
        print('\n    File renamed to: ' + newName + '\n')
    if newName[index:] != '.wav':       # check if it is a .wav file
        print('\n    Converted file from ' + newName[index:] + ' to .wav. \nNow referring to .wav file.\n')
        convert(newName, '.wav')
        newName = newName[:index] + '.wav'
    print('Name filtered to: ' + newName + '\n')
    return newName

def extensionIndex(speechFile):
    index = -1
    while speechFile[index] != '.' and index > -len(speechFile) + 1:
        index -= 1
    return index

def convert(speechFile, extension):
    import subprocess
    index = extensionIndex(speechFile)
    if not os.path.exists(speechFile[:index] + extension):
        #command = ['ffmpeg', "-i", speechFile, speechFile[:index] + extension]
        command = [
                   "ffmpeg", "-i", speechFile,
                   "-ab", "160k",
                   "-ac", "1",
                   "-vn", speechFile[:index] + extension
                  ]
        subprocess.call(command, shell=True)

file = 'Audio/obama.mp3'
newName = filterName(file)
subprocess.call(['bril.exe',
                 newName,
                 newName[:extensionIndex(file)] + '-edit' + newName[extensionIndex(file):],
                 '25'])
