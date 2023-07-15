import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch,random

from streamlit_chat import message

st.set_page_config(page_title="Jarvis", page_icon="🤖")

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

# Set the model engine and your OpenAI API key
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium") 

# sidebar()
footer()

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

# We will get the user's input by calling the get_text function
def get_text():
    integer = random.randint(1, 1000)
    input_text = st.text_input("You:",key=str(integer))
    return input_text

user_input = get_text()

# def generate_response(prompt):
        #new_user_input_ids = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors='pt')
        #bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
        #chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        #message = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        #return message 

while(True):   
    if user_input:
        new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        message = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        # store the output 
        st.session_state.past.append(user_input)
        st.session_state.generated.append(message)
        
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])-1, -1, -1):
                message(st.session_state["generated"][i], key=str(i))
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        user_input = False
    # user_input = get_text()
        