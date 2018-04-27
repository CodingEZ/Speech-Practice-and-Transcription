import pyaudio
import wave

def recordTo(file):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    recordTime = 60

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS, 
                        rate=RATE,
                        input=True,
                        output=True,
                        frames_per_buffer=CHUNK)

    frames = []
    print("Recording ... ", end="")
    for i in range(int(44100 / CHUNK * recordTime)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished!")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    file = wave.open('Audio/' + file, 'wb')
    file.setnchannels(CHANNELS)
    file.setsampwidth(audio.get_sample_size(FORMAT))
    file.setframeRATE(RATE)
    file.writeframes(b''.join(frames))
    file.close()
