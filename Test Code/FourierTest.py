"""Use of Fourier Transforms to acausally filter a signal."""
 
__author__ = 'Ed Tate'
__email__  = 'edtate<at>gmail-dot-com'
__website__ = 'exnumerus.blogspot.com'
__license__ = 'Creative Commons Attribute By - http://creativecommons.org/licenses/by/3.0/us/''' 


import pylab
from pydub import AudioSegment
import wave
from numpy.fft import fft, ifft
from numpy import array
import cmath

def almostEqual(num1, num2, delta=10**-7):
    num1 = cmath.polar(num1)[0]
    num2 = cmath.polar(num2)[0]
    return abs(num1, num2) < delta

def equalArray(array1, array2):
    if len(array1) != len(array2):
        return False
    for i in range(len(array1)):
        print(array1[i], array2[i])
        if almostEqual(array1, array2):
            return False
    return True

def filter_rule(sample, freq):
    """Filters a Fourier transformation by the following rule."""
    band = 0.05
    f_signal = 6
    if abs(freq) > f_signal + band or abs(freq) < f_signal - band:
        return 0
    else:
        return sample

def convertToArray(file, spliceName='Audio/OLD.wav', cutoff=1000):
    original = wave.open(file, 'rb')
    sound = AudioSegment.from_wav(file)[:cutoff]
    original.close()
    
    soundArray = sound.get_array_of_samples()
    frames_per_second = sound.frame_rate
    timeDif = 1 / frames_per_second
    sound.export(spliceName, 'wav')
    new = wave.open(spliceName, 'rb')
    parameters = new.getparams()
    return parameters, soundArray, timeDif

def convertToAudio(parameters, soundArray, fileName='Audio/NEW.wav'):
    file = wave.open(fileName, 'wb')
    file.setparams(parameters)
    file.writeframes(soundFiltered)
    file.close()

parameters, soundArray, timeDif = convertToArray("Audio/obama.wav")
#convertToAudio(parameters, soundArray)
'''
import math
transformLength = len(soundArray)

sinPart = [0] * transformLength
cosPart = [0] * transformLength
for index1 in range(transformLength):
    for index2 in range(transformLength):
        arg = 2 * index1 * math.pi * index2 / transformLength
        sinPart[index1] += soundArray[index2] * math.sin(arg) * (-1)
        cosPart[index2] += soundArray[index2] * math.cos(arg)

sampleRate = 0
frequency = [0] * transformLength//2
magnitude = [0] * transformLength//2
phase = [0] * transformLength//2
for i in range(transformLength//2):
    frequency[i] = i * sampleRate / transformLength
    magnitude[i] = 20 * math.log(2 * math.sqrt( sinPart[i]**2 + cosPart[i]**2 )) / transformLength
    phase[i] = 180 * math.atan(sinPart[i], cosPart[i]) / math.pi - 90
'''

soundArray = array(soundArray)
transformation = fft(soundArray)
print(soundArray[:100])
print(ifft(fft(soundArray))[:100])
assert( equalArray( soundArray, ifft(fft(soundArray)) ) )
