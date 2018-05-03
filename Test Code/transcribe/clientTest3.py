import io
from google.cloud import speech

client = speech.SpeechClient()
config = speech.types.RecognitionConfig(
    encoding='LINEAR16',
    language_code='en-US',
    sample_rate_hertz=44100,
)

with io.open('./hello.wav', 'rb') as stream:
    requests = [speech.types.StreamingRecognizeRequest(
        audio_content=stream.read(),
    )]
    
config = speech.types.StreamingRecognitionConfig(config=config)
responses = client.streaming_recognize(config,requests)
for response in responses:
    for result in response:
        for alternative in result.alternatives:
            print('=' * 20)
            print('transcript: ' + alternative.transcript)
            print('confidence: ' + str(alternative.confidence))
            print('is_final:' + str(result.is_final))
