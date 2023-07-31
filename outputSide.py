import requests
import base64
import time
import os
import streamlit as st

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/AZnzlk1XvdvUeBnXmlld"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "0ed0be1d1f638261788189c2afc57f33"
}


def generateAudio(text, voice_id, language_id):
    data = {
        "text": text,
        "model_id":"eleven_multilingual_v1", 
        "voice_id": voice_id,
        "language_id": language_id, 
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    response = requests.post(url, json=data, headers=headers)

    # Generate empty file
    with open("output.wav", 'wb') as file:
        pass
    
    # Save the response content to an .mp3 file
    output_file = "output.wav"
    
    with open(output_file, 'wb') as file:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                file.write(chunk)
    
    st.audio("output.wav", format='audio/wav')