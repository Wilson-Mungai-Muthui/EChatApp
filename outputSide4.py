import streamlit as st

def stream_audio(audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        st.audio(audio_file, format='audio/mp3', start_time=0)  # Set start_time to 0 to play from the beginning

audio_file_path = "output.mp3"  # Replace this with your audio file path

