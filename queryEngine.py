import openai
import os
import streamlit as st
from llama_index import StorageContext, load_index_from_storage
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.storage.index_store import SimpleIndexStore
from llama_index.vector_stores import SimpleVectorStore
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.retrievers import VectorIndexRetriever
from llama_index import get_response_synthesizer
from llama_index.indices.postprocessor import SimilarityPostprocessor
import time
from dotenv import load_dotenv

load_dotenv()

openai.api_key = st.secrets['OPENAI_API_KEY']

Base_dir = os.path.dirname(os.getcwd())
vectorIndexDir = os.path.join(Base_dir, "vector_index")

session_state = {}   #..Initialzing an empty dictionary to store key-value pairs

# Retrieve index from storage
storage_context = StorageContext.from_defaults(
    docstore=SimpleDocumentStore.from_persist_dir(persist_dir=vectorIndexDir),
    vector_store=SimpleVectorStore.from_persist_dir(persist_dir=vectorIndexDir),
    index_store=SimpleIndexStore.from_persist_dir(persist_dir=vectorIndexDir),
)

vector_index = load_index_from_storage(storage_context)

BaseRetriever = VectorIndexRetriever(
    index=vector_index,
    similarity_top_k=3,
)
# configure response synthesizer
response_synthesizer = get_response_synthesizer()

# Define engine chatbot
def Ecommerce_Chatbot(input_text):
    query_engine = RetrieverQueryEngine(
        retriever= BaseRetriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[
            SimilarityPostprocessor(similarity_cutoff=0.7)
    ])
    
    try:
        response = query_engine.query(input_text)
    except openai.error.RateLimitError as e:
        retry_time = 2  # e.retry_after if hasattr(e, 'retry_after') else 30
        print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        return Ecommerce_Chatbot(input_text)
    return response.response


def customEngine(prompt, chat_id='1'):
    promptConfig = f"""
    Identity: 
    You are a E-Commerce salesperson. Have your responses as humnan-like as possible meaning that  you should respond as a human would
    
    
    ' \nPrompt: \"\"\"{prompt}\"\"\" \n
   
    """
    prompt = promptConfig
    
    #   Keeping memory of the chat
    initial_context = {'system': promptConfig, 'user' : prompt, 'AI': ''}
    context = {}
    
    if chat_id not in session_state:
        context = initial_context
        session_state[chat_id] = []  # Initialize an empty list for chat_id
    else:
        context = {'user' : prompt, 'AI': ''}
    
    if len(session_state[chat_id]) == 2:
        session_state[chat_id] = []

    session_state[chat_id].append(context)
    context_string = f"\nsystem: {initial_context['system']}"

    for entry in session_state[chat_id]:
        context_string += f"\nuser: {entry['user']}\nAI: {entry['AI']}"
    response = Ecommerce_Chatbot(context_string)
    context = {'system': promptConfig, 'user': prompt, 'AI': response}
    session_state[chat_id].pop()
    session_state[chat_id].append(context)
    return response