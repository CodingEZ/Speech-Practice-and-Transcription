###############################################################################
# Following code was adapted from the google speech recognition documentation
'https://cloud.google.com/speech-to-text/docs/sync-recognize'
###############################################################################

import io
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def google_transcribe(speechFile):
    """Transcribe the given audio file. Apparently only takes files with
        parameters of a recorded file."""
    client = speech.SpeechClient()

    with io.open(speechFile, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=speech.Encoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US')

    transcript = ""
    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        #print('Transcript: {}'.format(result.alternatives[0].transcript))
        transcript += result.alternatives[0].transcript
    if len(transcript) > 0 and transcript[-1] == ' ':
        return transcript
    return transcript + ' '
