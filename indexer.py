import os
import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from llama_index import LLMPredictor, PromptHelper, ServiceContext, SimpleDirectoryReader, VectorStoreIndex, ListIndex
from llama_index.node_parser import SimpleNodeParser
from llama_index.langchain_helpers.text_splitter import TokenTextSplitter
from dotenv import load_dotenv

load_dotenv()

openai.api_key = st.secrets['OPENAI_API_KEY']

Base_dir = os.path.dirname(os.getcwd())
custom_path = os.path.join(Base_dir, "Jarvis")
llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
llm_predictor = LLMPredictor(llm=llm) 
node_parser = SimpleNodeParser(
  text_splitter=TokenTextSplitter(chunk_size=1024, chunk_overlap=20)
)
prompt_helper = PromptHelper(
  context_window=4096, 
  num_output=256, 
  chunk_overlap_ratio=0.3, 
  chunk_size_limit=None
)

service_context = ServiceContext.from_defaults(
  llm=llm,
  node_parser=node_parser,
  prompt_helper=prompt_helper
)

# Constructing the indices
def construct_index(directory_path):
    
    documents = SimpleDirectoryReader(directory_path).load_data()
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(documents)
    vectorIndex = VectorStoreIndex(nodes, service_context=service_context, show_progress=True)
    parent_dir = os.path.abspath(os.path.join(directory_path, os.pardir))
    vectorIndexDir = os.path.join(parent_dir, "vector_index")
    vectorIndex.storage_context.persist(persist_dir=vectorIndexDir)

    if vectorIndex:
        return True
    return False

construct_index("mpesa_docs")
