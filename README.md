# Speech-Practice-and-Transcription

This program is a Speech Practice and Transcription program, which has the  
capability to transcribe files from the computers and Youtube videos.
It also contains a practice in which you can practice recording a speech;
the program itself will record and transcribe what you say and check for 
differences with a given script. In this way, one can find errors and
practice until they get 100% correct. 

## Requirements
The project requires a number of libraries, which are listed below.

1. Python 3.x (most compatible with the other modules)
2. Google Speech Recognition API
	- imported from google.cloud
3. PyQt5
4. pydub
5. pyaudio, wave
6. pytube
7. subprocess
8. pillow
9. sys, os, io
The last few libraries as well as additional libraries come with existing
packages (math, string, etc.).

In order to get Google Speech Recognition working follow the instructions
in the following link:
	https://cloud.google.com/speech-to-text/docs/reference/libraries

You will need to create a client account in order to obtain the necessary
authentication. When you have obtained the authentication files, insert
the file name into your code in the Transcribe.py file as:
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = YOURFILENAME

The other libraries can be installed using pip (pip install) from terminal.

## How to use this repo
The way to use this program is to run the main.py file, which opens up a
new PyQt5 widget window in which everything is contained. Besides that, 
there are instruction on inner pages. One thing to note is that the 
program will display messages after the operation is finished, so the user 
will have to wait for the recording period to finish and for transcribing 
to finish.
