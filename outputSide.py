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
  "xi-api-key": "1e92a485fb5c011d58945119747807fc"
}

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        '''st.markdown(
            md,
            unsafe_allow_html=True,
        )'''

def generateAudio(text, model_id, language_id):
    data = {
        "text": text,
        "model_id": model_id,
        "language_id": language_id, 
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    response = requests.post(url, json=data, headers=headers)

    # Generate empty file
    with open("output.mp3", 'wb') as file:
        pass
    
    # Save the response content to an .mp3 file
    output_file = "output.mp3"
    
    with open(output_file, 'wb') as file:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                file.write(chunk)
    
    # autoplay_audio("output.mp3")
    st.audio("output.mp3")