import requests
import validators
import streamlit as st
from bs4 import BeautifulSoup
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents import create_react_prompt
from langchain_groq import ChatGroq 
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def process_url(url):
    
    if not validators.url(url):
        st.error("Invalid URL. Please enter a valid URL.")
        return None
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content,'html.parser')
        text_data = soup.get_text(separator='\n')            # Extract text from the page

    except Exception as e:
        st.error(f"An error occurred while scraping the URL: {e}")
        return None
    
    return text_data



def text_splitter(text_data):
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1500, chunk_overlap=200)
    docs = text_splitter.split_text(text_data)
    return docs



def create_vector_db(docs):
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_texts(docs, embedding_model)
    return db
    



def get_llm():
    llm = ChatGroq(
      model_name = "llama-3.1-70b-versatile",
      groq_api_key = GROQ_API_KEY,
      temperature= 0
    )
    return llm
    
    
    
def retriever(vector_db):
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    return retriever
    


# def zero_shot_agent(tools, llm, PROMPT, question):

#     zero_shot_Agent = initialize_agent(
#         agent="zero-shot-react-description",
#         tools=tools,
#         prompt=PROMPT,
#         llm=llm,
#         verbose=True,
#         max_iterations=3
#     )

#     agent_Executer = AgentExecutor(
#         agent=zero_shot_Agent,
#         tools=tools
#     )
    
#     response = agent_Executer.invoke({
#         "input" : question,
#     })
    
#     return response

def zero_shot_agent(tools, llm, question):
    # 1. Create a prompt
    # prompt = ChatPromptTemplate.from_messages(PROMPT)
    prompt = create_react_prompt(tools)
    # 2. Create a REACT style agent
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    # 3. Wrap it with an executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # 4. Now run it
    response = agent_executor.invoke({
        "input": question,
    })

    return response