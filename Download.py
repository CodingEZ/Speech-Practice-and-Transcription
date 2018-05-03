from pytube import YouTube
import os
import string

def firstNameSplice(file):
    letterSet = set(string.ascii_letters)
    index = 0
    while file[index] in letterSet:
        index += 1
    return file[:index]

def secondNameSplice(file):
    letterSet = set(string.ascii_letters)
    index = 0
    while file[index] in letterSet:
        index += 1
    while file[index] not in letterSet:
        index += 1
    index2 = index
    while index2 < len(file) and file[index2] in letterSet:
        index2 += 1
    if index2 == len(file):
        return None
    return file[index:index2]

def extensionSplice(file):
    """Helper that finds the index for the extension of a file."""
    index = -1
    while file[index] != '.' and index > -len(file) + 1:
        index -= 1
    return file[index:]

def shortenName(name):
    components = name.split('/')
    fileName = components[-1]

    firstName = firstNameSplice(fileName)
    secondName = secondNameSplice(fileName)
    extension = extensionSplice(fileName)
    if secondName == None:
        components[-1] = firstName + extension
    else:
        components[-1] = firstName + '-' + secondName + extension
    return '/'.join(components)

def downloadYoutube(url):
    dirList = os.listdir('Audio')
    try:        handle = YouTube(url)
    except:     return 0

    try:        handle.streams.first().download('Audio')
    except:     return 1

    for file in os.listdir('Audio'):
        if file not in dirList:
            name = shortenName('Audio/' + file)
            os.rename('Audio/' + file, name)
            return name
