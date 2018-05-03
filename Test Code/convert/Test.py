import subprocess
command = "ffmpeg -i Audio/Satisfied.mp3 Audio/Clean Bandit-Rockabye/Satisfied.wav"
subprocess.call(command, shell=True)

'''
from pydub import AudioSegment

location = "Audio\\Clean Bandit-Rockabye.wav"
sound = AudioSegment.from_wav(location)
'''
