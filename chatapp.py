import streamlit as st
import openai
import os
from audio_recorder_streamlit import audio_recorder
from streamlit_chat import message
from dotenv import load_dotenv
from outputSide import generateAudio
from queryEngine import customEngine
from translate import convert

load_dotenv()

openai.api_key = st.secrets['OPENAI_API_KEY']

st.set_page_config(page_title="E-Commerce Chat Bot", page_icon="", layout="wide")

col1, col2, col3 = st.columns(3)
with col2:
    st.image("https://afrineuron.files.wordpress.com/2023/06/afrineuron-1-10-2.png")
    
st.markdown("<h2 style='text-align: center;'>E-Commerce Chat Bot</h1>", unsafe_allow_html=True)

def footer():
    hide_streamlit_style = """
                <style>
                footer {visibility: hidden;}              
                footer:after {
                    content:'Powered by Afrineuron'; 
                    visibility: visible;
                    display: block;
                    position: right;
                    #background-color: red;
                    padding: 5px;
                    top: 2px;
                    .sidebar .sidebar-content {
                    background-image: linear-gradient(#2e7bcf,#2e7bcf);
                    color: white;}
            }
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

footer()

with st.sidebar:
    st.markdown('## Chat Settings\n')
    voice = st.selectbox("Choose Sales Agent", ("Rachel", "Clyde", "Bella", "Dave", "Antoni", "Emily", "Patrick", "Harry", "Dorothy", "Arnold", "Charlotte", "Joseph", "Ethan", "Gigi", "Serena", "Adam", "Nicole", "Ryan", "Glinda", "Giovanni"))
    language = st.selectbox("Choose Language", ("English", "Deutsch", "Polish", "Spanish", "Italian", "French", "Portugese", "Hindi"))
    
                            
st.session_state['generated'] = []
st.session_state['past'] = []

audio_file_1 = audio_recorder(text="Click to speak",  icon_size="1x", pause_threshold=1.0, sample_rate=41_000)

if audio_file_1:
    # To play audio in frontend:
    #st.audio(audio_file_1.tobytes())
        
    # To save audio to a file:
    with open("_audio_1.mp3", "wb") as f:
        f.write(audio_file_1)

audio_file= open("_audio_1.mp3", "rb")

transcript = openai.Audio.transcribe("whisper-1", audio_file)
# st.markdown (transcript["text"])

# Button to reset conversation
if st.button("Reset Conversation"):
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.stop()

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

# Function to generate a response using OpenAI GPT-3.5 with a persona
def generate_response(prompt):
    messages = [
        {"role": "system", "content": 'You are a sales assistant. Respond in 50 words or less.'},
        {"role": "user", "content": prompt},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.8,
    )
    return response.choices[0].message['content'].strip()

if transcript:
    transcript = transcript["text"]
    output = customEngine(transcript, chat_id='1')
    if language == 'English':
        with st.spinner("Converting into Audio..."):
            generateAudio(output,voice)
    else:
        with st.spinner("Translating your context"):
            language_translation = convert("en",language,output)
            with st.spinner("Converting into Audio..."):
                generateAudio(language_translation,voice)
                
    # store the output 
    st.session_state.past.append(transcript)
    st.session_state.generated.append(output)
    st.markdown("<h6 style='text-align: center;'>Play Audio Response </h1>", unsafe_allow_html=True)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            
