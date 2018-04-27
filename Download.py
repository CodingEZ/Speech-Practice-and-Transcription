from pytube import YouTube
import os

def downloadYoutube(url):
    dirList = os.listdir('Audio')
    try:        handle = YouTube(url)
    except:     return 0

    try:        handle.streams.first().download('Audio')
    except:     return 1

    for file in os.listdir('Audio'):
        if file not in dirList:
            name = 'Audio/' + file
            return name
