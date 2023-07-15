# Importing required packages
import streamlit as st
from streamlit.logger import get_logger
import openai
from dotenv import load_dotenv
import os

load_dotenv()
logger = get_logger(__name__)
  
from streamlit_chat import message

st.set_page_config(page_title="Jarvis", page_icon="🤖", layout="wide")

col1, col2, col3 = st.columns(3)
with col2:
    st.image("https://afrineuron.files.wordpress.com/2023/06/afrineuron-1-10-2.png")
    
st.markdown("<h1 style='text-align: center; color: white;'>Jarvis AI Chatbot🤖</h1>", unsafe_allow_html=True)

def footer():
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}              
                footer:after {
                    content:'Powered by Afrineuron'; 
                    visibility: visible;
                    display: block;
                    position: centre;
                    #background-color: red;
                    padding: 5px;
                    top: 2px;
                    .sidebar .sidebar-content {
                    background-image: linear-gradient(#2e7bcf,#2e7bcf);
                    color: white;}
            }
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def sidebar():
    with st.sidebar:
        
        st.markdown(
            "## Instructions\n" 
        )
        st.sidebar.info(
        '''This is a web application that allows you to interact with 
       the OpenAI API's implementation of the ChatGPT model.
       Enter a **query** in the **text box** and **press enter** to receive 
       a **response** from the ChatGPT
       '''
        )
        st.markdown("---")
        st.markdown(
            "## How to use\n"
            "Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
        )
        openai_api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=os.environ.get("OPENAI_API_KEY", None)
            or st.session_state.get("OPENAI_API_KEY"),
        )

        #st.session_state["OPENAI_API_KEY"] = api_key_input

        st.markdown("---")
        return openai_api_key


# Set the model engine and your OpenAI API key
model_engine = "text-davinci-003"
# openai.api_key = "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" 

sidebar()
footer()

openai_api_key = st.session_state.get("OPENAI_API_KEY")

if not openai_api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )

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

if not is_open_ai_key_valid(openai_api_key):
    st.stop()

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def generate_response(prompt):
    completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message 

# We will get the user's input by calling the get_text function
def get_text():
    input_text = st.text_input("You: ","Hello, how are you?", key="input")
    return input_text

user_input = get_text()

if user_input:
    output = generate_response(user_input)
    # store the output 
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
    
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')