import google

def explicit():
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the
    # private key file.
    storage_client = storage.Client.from_service_account_json(
        'Youtube Transcript Translator-1afc5757090d.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

#explicit()

#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
 
import speech_recognition as sr
 
# Record Audio
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=1)
    print("Say something!")
    audio = r.listen(source, phrase_time_limit=5)
    print("Audio cut off.")
 
# Speech recognition using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("You said: " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
