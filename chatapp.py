import streamlit as st
import openai
import os
from audio_recorder_streamlit import audio_recorder
from streamlit_chat import message
from streamlit.logger import get_logger
from dotenv import load_dotenv
from outputSide import generateAudio


#openai.api_key = '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'
logger = get_logger(__name__)
load_dotenv()

st.set_page_config(page_title="Multilingual Voice AI Model", page_icon="", layout="wide")

col1, col2, col3 = st.columns(3)
with col2:
    st.image("https://afrineuron.files.wordpress.com/2023/06/afrineuron-1-10-2.png")
    
st.markdown("<h1 style='text-align: center; color: white;'>Multilingual Voice AI Model</h1>", unsafe_allow_html=True)

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
    api_key_input = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="Paste your OpenAI API key here (sk-...)",
    help="You can get your API key from https://platform.openai.com/account/api-keys.",
    value=os.environ.get("OPENAI_API_KEY", None)
    or st.session_state.get("OPENAI_API_KEY", ""),
    )
    st.session_state["OPENAI_API_KEY"] = api_key_input
    st.caption("*If you don't have an OpenAI API key, get it [here](https://platform.openai.com/account/api-keys).*")

footer()

'''@st.cache_data(show_spinner=False)
def is_open_ai_key_valid(openai_api_key) -> bool:
    if not openai_api_key:
        st.error("Please enter your OpenAI API key in the sidebar!")
        return False
    try:
        openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            api_key=openai_api_key,
        )
    except Exception as e:
        st.error(f"{e.__class__.__name__}: {e}")
        logger.error(f"{e.__class__.__name__}: {e}")
        return False
    return True

openai.api_key = st.session_state.get("OPENAI_API_KEY")

if not openai.api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )

if not is_open_ai_key_valid(openai.api_key):
    st.stop()

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

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

# Function to generate a response using OpenAI GPT-3.5 with a persona
def generate_response(prompt):
    messages = [
        {"role": "system", "content": 'You are a sales assistant. Respond in 40 words or less.'},
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
    generateAudio(output)
    # store the output 
    st.session_state.past.append(transcript)
    st.session_state.generated.append(output)
    
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')'''
            
