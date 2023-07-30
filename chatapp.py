import streamlit as st
import openai

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
model_engine = "gpt-3.5-turbo"
openai.api_key = "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" 

# sidebar()
footer()

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def generate_response(prompt):
    completions = openai.Completion.create(
        engine = "gpt-3.5-turbo",
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature=0.9,
    )
    message = completions.choices[0].text
    return message 

# We will get the user's input by calling the get_text function
def get_text():
    input_text = st.text_input("You:", key="input")
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