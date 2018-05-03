import io
from google.cloud import speech

client = speech.SpeechClient()
config = speech.types.RecognitionConfig(
    encoding='LINEAR16',
    language_code='en-US',
    sample_rate_hertz=44100,
)

with io.open('./hello-pause-goodbye.wav', 'rb') as stream:
    requests = [speech.types.StreamingRecognizeRequest(
        audio_content=stream.read(),
    )]

results = sample.streaming_recognize(
    config=speech.types.StreamingRecognitionConfig(
        config=config,
        single_utterance=False,
    ),
    requests,
)

for result in results:
    for alternative in result.alternatives:
        print('=' * 20)
        print('transcript: ' + alternative.transcript)
        print('confidence: ' + str(alternative.confidence))

