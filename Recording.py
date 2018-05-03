import pyaudio
import wave

def recordTo(file, app, PERIOD=10):
    """Loosely based off existing recording code with pyaudio."""
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, output=True, frames_per_buffer=CHUNK)

    frames = []
    app.resetLog()
    app.updateLog(" Recording ... ")
    for i in range(int(44100 / CHUNK * PERIOD)):
        data = stream.read(CHUNK)
        frames.append(data)
    app.updateLog("Finished!\n")

    stream.stop_stream()        # stop stream when finished
    stream.close()
    audio.terminate()

    file = wave.open(file, 'wb')        # save to a file
    file.setnchannels(CHANNELS)
    file.setsampwidth(audio.get_sample_size(FORMAT))
    file.setframerate(RATE)
    file.writeframes(b''.join(frames))
    file.close()
