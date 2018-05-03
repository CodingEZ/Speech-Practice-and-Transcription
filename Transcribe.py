import os
import io
from pydub import AudioSegment
import copy
from GoogleTranscribe import *
from Converter import *

SPLICELEN = 60000       # for now, only up to 60 seconds per splice
PATCHLEN = 10000
TEXTLEN = 75
SPLICE = '/splice.'
PATCH = '/patch.'
INSIDEPATCH = '/insidepatch.'
SPLITPATCH1 = '/splitpatch1.'
SPLITPATCH2 = '/splitpatch2.'
FILENAMES = [SPLICE, PATCH, INSIDEPATCH, SPLITPATCH1, SPLITPATCH2]

# sets up credentials to allow someone who holds the required json file to use speech recognition
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Youtube Transcript Translator-1afc5757090d.json"


def filterName(speechFile, app):
    """Filters the file name and converts it into a .wav file.
        Also filters the file itself of most constant background noise."""
    app.updateLog(' Filtering name: ' + speechFile)
    if not isFile(speechFile, app):
        return None
    newName = speechFile.replace(" ", "-")
    index = extensionIndex(newName)

    if newName != speechFile:
        os.rename(speechFile, newName)      # renames the original file
        app.updateLog('\n    Renamed to: ' + newName)
    if newName[index:] != '.wav':       # check if it is a .wav file
        app.updateLog('\n    Converted file from ' + newName[index:] + ' to .wav. Referring to .wav file.')
        newName = convert(newName, '.wav')      # convert to .wav file
    newName = convertClean(newName, '.wav')
    app.updateLog('\n    Name filtered to: ' + newName + '\n')
    return newName

def isFile(speechFile, app):
    if not os.path.isfile(speechFile):
        app.updateLog('    Not a file! Please input a file\n')
        return False
    return True

def extensionIndex(speechFile):
    """Helper that finds the index for the extension of a file."""
    index = -1
    while speechFile[index] != '.' and index > -len(speechFile) + 1:
        index -= 1
    return index

def mkFilesLocation(speechFile, app):
    """Makes a new folder if one does not already exist."""
    end = extensionIndex(speechFile)
    folder = speechFile[:end]
    if not os.path.exists(folder):
        app.updateLog(' Made new directory.\n')
        os.mkdir(folder)

def divide_files(speechFile, sound, length, app):
    """Splices a given file and creates the corresponding patches."""
    def export(name, startSound, endSound, index, FORMAT='wav'):
        try:    newSound = sound[startSound:endSound]
        except: newSound = sound[startSound:]
        newSound.export(folder + name + str(index) + '.' + FORMAT, format=FORMAT)
    
    app.updateLog(' Started division ... ')
    end = extensionIndex(speechFile)
    folder = speechFile[:end]

    for i in range(int(length // (SPLICELEN//1000))):
        export(SPLICE, i*SPLICELEN, (i+1)*SPLICELEN, i)
        export(PATCH, (i+1)*SPLICELEN - PATCHLEN//2, (i+1)*SPLICELEN + PATCHLEN//2, i)
        export(INSIDEPATCH, (i+1)*SPLICELEN - PATCHLEN//4, (i+1)*SPLICELEN + PATCHLEN//4, i)
        export(SPLITPATCH1, (i+1)*SPLICELEN - PATCHLEN//2, (i+1)*SPLICELEN, i)
        export(SPLITPATCH2, (i+1)*SPLICELEN, (i+1)*SPLICELEN + PATCHLEN//2, i)
    app.updateLog('Finished.\n')

def reparameter_files(speechFile, length, app):
    """Overlays a file to allow transcription by the Google API."""
    def replace(name, index, FORMAT='wav'):
        fileName = folder + name + str(index) + '.' + FORMAT
        if os.path.exists(fileName):
            segment = AudioSegment.from_wav(fileName)
            duration = segment.duration_seconds * 1000
            os.remove(fileName)
            combined = basis[:duration].overlay(segment)
            combined.export(fileName, FORMAT)
    
    app.updateLog(' Started reparameterization ... ')
    end = extensionIndex(speechFile)
    folder = speechFile[:end]
    
    basis = AudioSegment.from_wav('Audio/basis.wav')
    basis = basis[:SPLICELEN] - 100       # reduce volume of basis by 100 decibels
    for i in range(int(length // (SPLICELEN//1000))):
        replace(SPLICE, i)
        replace(PATCH, i)
        replace(INSIDEPATCH, i)
        replace(SPLITPATCH1, i)
        replace(SPLITPATCH2, i)
    app.updateLog('Finished.\n')

def rmFilesLocation(speechFile, app):
    """Removes the folder of splices and patch in case of an error."""
    end = extensionIndex(speechFile)
    folder = speechFile[:end]
    if len(os.listdir(folder)) == 0:
        os.rmdir(folder)
        app.updateLog(' Removed empty folder.\n')
    else:
        app.updateLog(' Failed to removed filled folder.\n')

def remove_files(speechFile, length, app):
    """Removes splice and patch files."""
    def remove(name, index, extension='.wav'):
        fileName = folder + name + str(index) + extension
        if os.path.exists(fileName):
            os.remove(fileName)
    
    app.updateLog(' Started file removal ... ')
    end = extensionIndex(speechFile)
    folder = speechFile[:end]
    
    for i in range(int(length // (SPLICELEN//1000))):
        for filename in FILENAMES:
            remove(filename, i)
    app.updateLog('Finished.\n')

def match_words(outerWords, innerWords, middleIndex):
    """Helper that finds the largest section of intersecting words."""
    startIndex = middleIndex
    while (outerWords[startIndex] in innerWords) and startIndex > 0:
        startIndex -= 1
    startIndex += 1

    endIndex = middleIndex
    while (outerWords[endIndex] in innerWords) and endIndex < len(outerWords) - 1:
        endIndex += 1
    return outerWords[startIndex:endIndex]

def match_patch(fullPatch, folder, index):
    """Finds words in the inner patch that also belong to the outer patch.
        Used as the main patch to knit together splices."""
    patchWords = fullPatch.lower().split(" ")
    middleWordIndex = len(patchWords)//2
    insidePatch = transcribe_one(INSIDEPATCH, folder, index).lower()
    insidePatchWords = insidePatch.split(" ")
    if patchWords[middleWordIndex] not in insidePatchWords:
        # check other patches for words
        splitPatch1 = transcribe_one(SPLITPATCH1, folder, index).lower()
        splitPatch1Words = splitPatch1.split(" ")
        if patchWords[middleWordIndex] in splitPatch1Words:
            return match_words(patchWords, splitPatch1Words, middleWordIndex)
        
        splitPatch2 = transcribe_one(SPLITPATCH2, folder, index).lower()
        splitPatch2Words = splitPatch2.split(" ")
        if patchWords[middleWordIndex] in splitPatch2Words:
            return match_words(patchWords, splitPatch2Words, middleWordIndex)
        return patchWords # returns the entire patch if nothing can be found
    
    return match_words(patchWords, insidePatchWords, middleWordIndex)

def match_start(fullTranscript, matches):
    """Helper that knits the previous splice with the next patch."""
    copyMatches = copy.copy(matches)
    copyScript = fullTranscript[-TEXTLEN:]
    endScript = copyScript[copyScript.find(' ')+1:].lower()
    while len(copyMatches) > 1:
        place = endScript.find(copyMatches[0] + ' ' + copyMatches[1])
        if place == -1:
            copyMatches.pop(0)      # case of bad translation at beginning of insidePatch
        elif place == 0 or (place  != 0 and endScript[place-1] == ' '):
            #  and endScript[place + len(matches[0]) + len(matches[1]) + 2] == ' ', potential error
            return place + copyScript.find(' ')
        else:
            while place != endScript[place+1:].find(copyMatches[0] + ' ' + copyMatches[1]) + place + 1:
                place = endScript[place+1:].find(copyMatches[0] + ' ' + copyMatches[1]) + place + 1
                if endScript[place-1] == ' ':
                    return place + copyScript.find(' ')
            copyMatches.pop(0)
        place = 0
    return None

def match_end(nextTranscript, matches):
    """Helper that knits a patch with the next splice."""
    copyMatches = copy.copy(matches)
    copyScript = nextTranscript[:TEXTLEN][::-1]
    startScript = copyScript[copyScript.find(' ')+1:].lower()
    while len(copyMatches) > 1:
        place = startScript.find(copyMatches[-1][::-1] + ' ' + copyMatches[-2][::-1])
        if place == -1:
            copyMatches.pop()      # case of bad translation at beginning of insidePatch
        elif place == 0 or (place  != 0 and startScript[place-1] == ' '):
            return place + copyScript.find(' ')
        else:
            while place != startScript[place+1:].find(copyMatches[-1][::-1] + ' ' + copyMatches[-2][::-1]) + place + 1:
                place = startScript[place+1:].find(copyMatches[-1][::-1] + ' ' + copyMatches[-2][::-1]) + place + 1
                if startScript[place-1] == ' ':
                    return place + copyScript.find(' ')
            copyMatches.pop()
        place = TEXTLEN
    return None

def transcribe_one(name, folder, index, extension='.wav'):
    """Transcribes a single file."""
    fileName = folder + name + str(index) + extension
    if os.path.exists(fileName):
        transcript = google_transcribe(fileName)
        return transcript
    return ""

def develop_transcript(folder, length):
    """Develops the transcript by taking file splices and patching them together."""
    fullTranscript = transcribe_one(SPLICE, folder, 0)  # start fullTranscript
    for i in range(int(length // (SPLICELEN//1000))):
        if i != int(length // (SPLICELEN//1000)) - 1:     # checks if there is a next transcript
            nextTranscript = transcribe_one(SPLICE, folder, i+1)
        else:
            nextTranscript = ""     # last add does not add a section
            
        fullPatch = transcribe_one(PATCH, folder, i).lower()
        if fullPatch == "":     continue

        matches = match_patch(fullPatch, folder, i)
        if len(matches) != 0:
            # for patching first part
            place = match_start(fullTranscript, matches)
            if place != None:       fullTranscript = fullTranscript[ : place-TEXTLEN]
            # for patching next part
            place = match_end(nextTranscript, matches)
            if place != None:       nextTranscript = nextTranscript[TEXTLEN-place : ]
        
        fullTranscript = ' '.join([fullTranscript] + matches + [nextTranscript])
    return fullTranscript

def transcribe_files(speechFile, length, app):
    """Checks is the given file exists and calls develop_transcript."""
    app.updateLog(' Started transcription ... ')
    end = extensionIndex(speechFile)
    folder = speechFile[:end]

    if not os.path.exists(speechFile):
        app.updateLog('File does not exist, cannot call transcription.\n')
        return

    fullTranscript = develop_transcript(folder, length) # develop transcript
    file = open(folder + '/transcription.txt', 'w')
    file.write(fullTranscript)
    app.updateLog('Finished.\n')

def simple_transcribe(speechFile, app):
    """Transcribes a file less than the maximum length of a splice."""
    app.updateLog(' Started transcription ... ')
    end = extensionIndex(speechFile)
    folder = speechFile[:end]
    
    if not os.path.exists(speechFile):  # check file existence
        app.updateLog('File does not exist, cannot call transcription.\n')
        return

    fullTranscript = google_transcribe(speechFile)  # directly translate the file
    file = open(folder + '/transcription.txt', 'w')
    file.write(fullTranscript)
    app.updateLog('Finished.\n')

def full_transcribe(file, app, willRemove=True, cutoff=None):
    """Call for the full transcription of any video or audio file.
        Emphasizes safety to make sure program does not crash."""

    app.updateLog(' Transcribing the following file: ' + file + '\n')
    try:
        file = filterName(file, app)
    except:
        return 'Error in filtering name!'

    try:
        if cutoff == None:
            sound = AudioSegment.from_wav(file)
        else:
            sound = AudioSegment.from_wav(file)[:cutoff]
        length = sound.duration_seconds
    except:
        return 'Error in determining length'

    try:
        mkFilesLocation(file, app)
    except:
        return 'Error in making files location!'

    try:
        divide_files(file, sound, length, app)
    except:
        if willRemove:
            remove_files(file, length, app)
            rmFilesLocation(file, app)
        return 'Error in dividing files!'

    try:
        reparameter_files(file, length, app)
    except:
        if willRemove:
            remove_files(file, length, app)
            rmFilesLocation(file, app)
        return 'Error in reparametering files!'

    try:
        if length > SPLICELEN//1000:
            transcribe_files(file, length, app)
        else:
            simple_transcribe(file, app)
    except:
        if willRemove:
            remove_files(file, length, app)
            rmFilesLocation(file, app)
        return 'Error in transcription!'
    
    if willRemove:
        remove_files(file, length, app)
    return None
