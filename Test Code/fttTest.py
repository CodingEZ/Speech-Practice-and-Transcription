"""
Script to demonstrate the use of Fourier Transforms to acausally filter a signal.
"""
 
__author__ = 'Ed Tate'
__email__  = 'edtate<at>gmail-dot-com'
__website__ = 'exnumerus.blogspot.com'
__license__ = 'Creative Commons Attribute By - http://creativecommons.org/licenses/by/3.0/us/''' 
 
 
from pylab import *

# setup the problem
sampleNum  = 1000 # number of samples

# generate an ideal signal
f_signal = 6   # signal frequency  in Hz
timeDif = 0.01 # sample timing in sec
phaseShift = 30   # 30 degrees of phase shift
amplitude = 1    # signal amplitude
s = [amplitude * sin((2*pi)*f_signal*k*timeDif) for k in range(0, sampleNum)]
s_time = [k*timeDif for k in range(0, sampleNum)]
 
# simulate measurement noise
from random import gauss
mu = 0
sigma = 2
n = [gauss(mu, sigma) for k in range(0, sampleNum)]
 
# measured signal
s_measured = [ss+nn for ss, nn in zip(s, n)]

# take the fourier transform of the data
F = fft(s_measured)
     
# calculate the frequencies for each FFT sample
f = fftfreq(len(F), timeDif)  # get sample frequency in cycles/sec (Hz)
 
# filter the Fourier transform
def filter_rule(x, freq):
    band = 0.05
    if abs(freq) > f_signal + band or abs(freq) < f_signal - band:
        return 0
    else:
        return x
         
F_filtered = array([filter_rule(x, freq) for x, freq in zip(F, f)])
 
# reconstruct the filtered signal
s_filtered = ifft(F_filtered)
 
# get error
err = [abs(s1-s2) for s1, s2 in zip(s, s_filtered) ]
 
figure()
subplot(4, 1, 1)
plot(s_time, s)
ylabel('Original Signal')
xlabel('time [s]')
 
subplot(4, 1, 2)
plot(s_time, s_measured)
ylabel('Measured Signal')
xlabel('time [s]')
 
subplot(4, 1, 3)
semilogy(f,abs(F_filtered), 'or')
semilogy(f,abs(F), '.')
legend(['Filtered Spectrum', 'Measured Spectrum',])
xlabel('frequency [Hz]')
 
subplot(4, 1, 4)
plot(s_time,s_filtered, 'r')
plot(s_time, s, 'b')
legend(['Filtered Signal', 'Original Signal'])
xlabel('time [s]')

show()
