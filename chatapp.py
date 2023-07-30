import streamlit as st
import openai
import os
from audio_recorder_streamlit import audio_recorder
from streamlit_chat import message
from streamlit.logger import get_logger
from dotenv import load_dotenv
from outputSide import generateAudio

st.write("Hello World")
