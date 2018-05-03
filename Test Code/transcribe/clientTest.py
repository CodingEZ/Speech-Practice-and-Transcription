from google.cloud import speech

client = speech.SpeechClient()

operation = client.long_running_recognize(
    audio=speech.types.RecognitionAudio(
        uri='gs://my-bucket/recording.flac',
        # uri is location of file in google cloud recording
    ),
    config=speech.types.RecognitionConfig(
        encoding='LINEAR16',
        language_code='en-US',
        # extra 1
        '''
        profanity_filter=True,
        '''
        # extra 2
        '''
        speech_contexts=[speech.types.SpeechContext(
                phrases=['hi', 'good afternoon'],
                )],
        '''
        sample_rate_hertz=44100,
    ),
)

op_result = operation.result()
for result in op_result.results:
    for alternative in result.alternatives:
        print('=' * 20)
        print('transcript: ', alternative.transcript)
        print('confidence: ', alternative.confidence)
