import streamlit as st
import openai
import os
from audio_recorder_streamlit import audio_recorder
from streamlit_chat import message
from dotenv import load_dotenv
from outputSide import generateAudio

#openai.api_key = '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'
#openai.api_key = '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'

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="E-Commerce Chat Bot", page_icon="", layout="wide")

col1, col2, col3 = st.columns(3)
with col2:
    st.image("https://afrineuron.files.wordpress.com/2023/06/afrineuron-1-10-2.png")
    
st.markdown("<h1 style='text-align: center; color: white;'>E-Commerce Chat Bot</h1>", unsafe_allow_html=True)

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

with st.sidebar:
    st.markdown('## Instructions\n')
    voice_id = st.selectbox("Choose Sales Agent", ({"Rachel":"21m00Tcm4TlvDq8ikWAM", "Clyde":"2EiwWnXFnvU5JabPnv8n", "Bella":"EXAVITQu4vr4xnSDxMaL", "Dave":"CYw3kZ02Hs0563khs1Fj", "Antoni": "ErXwobaYiN019PkySvjV", "Emily":"LcfcDJNUP1GQjkzn1xUU", "Patrick": "ODq5zmih8GrVes37Dizd", "Harry":"SOYHLrjzK2X1ezoPC6cr", "Dorothy":"ThT5KcBeYPX3keUQqHPh", "Arnold":"VR6AewLTigWG4xSOukaG", "Charlotte":"XB0fDUnXU5powFXDhCwa", "Joseph":"Zlb1dXrM653N07WRdFW3", "Ethan":"g5CIjZEefAph4nQFvHAz", "Gigi":"jBpfuIE2acCO8z3wKNLl", "Serena":"pMsXgVXv3BLzUgSXRplE", "Adam":"pNInz6obpgDQGcFmaJgB", "Nicole":"piTKgcLEGmPE4e6mEKli", "Ryan":"wViXBPUzp2ZZixB1xQuM", "Glinda":"z9fAnlkpzviPz146aGWa", "Giovanni":"zcAOhNBS3c14rBihAFp1"}))
    language_id = st.selectbox("Choose Language", ({"English":"en", "Deutsch":"de", "Polish":"pl", "Spanish":"es", "Italian":"it", "French":"fr", "Portugese":"pt", "Hindi":"hi"}))
    

footer()

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
    output = generate_response(transcript)
    generateAudio(output, voice_id, language_id)
    # store the output 
    st.session_state.past.append(transcript)
    st.session_state.generated.append(output)
    st.markdown("<h5 style='text-align: center;'>Play Audio Response </h1>", unsafe_allow_html=True)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            
