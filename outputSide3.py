import streamlit as st
from pydub import AudioSegment
import os

def convert_audio_to_wav(audio_file):
    # Load the audio file using pydub
    audio = AudioSegment.from_file(audio_file)
    
    # Check if the file is not already in WAV format
    if not audio_file.lower().endswith('.wav'):
        # If it's not in WAV format, convert it to WAV
        new_audio_file = audio_file.replace('.mp3', '.wav')
        audio.export(new_audio_file, format='wav')
        return new_audio_file
    else:
        # If it's already in WAV format, return the original path
        return audio_file

currentlocation = os.getcwd()

def playAudio(audio_file):
    if audio_file:
        # Convert the audio file to WAV format using pydub
        converted_file = convert_audio_to_wav(audio_file)

        # Play the converted audio using Streamlit's audio player
        st.audio(converted_file, format='audio/wav')

