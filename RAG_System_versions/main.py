import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import openai

def fetch_and_parse(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([para.get_text() for para in paragraphs])
        return text
    else:
        st.error(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return ""

def main():
    st.title('🦜🔗 Chat With Website')
    st.subheader('Input your website URL, ask questions, and receive answers directly from the website.')
    
    # Collecting user inputs
    key = st.text_input("Insert Your OpenAI API Key", type="password")
    url = st.text_input("Insert The website URL")
    question = st.text_input("Ask a question (query/prompt)")

    if st.button("Submit Query", type="primary"):
        if not key:
            st.error("Please provide your OpenAI API key.")
            return
        
        # Set API key
        openai.api_key = key
        os.environ['OPENAI_API_KEY'] = key

        # Define paths
        ABS_PATH = os.path.dirname(os.path.abspath(__file__))
        DB_DIR = os.path.join(ABS_PATH, "db")

        # Fetch and process website data
        data = fetch_and_parse(url)
        if not data:
            st.error("Failed to load data from the website.")
            return

        # Split documents
        text_splitter = CharacterTextSplitter(separator='\n', chunk_size=100, chunk_overlap=40)
        docs = text_splitter.split_documents([data])

        # Create embeddings and vector database
        openai_embeddings = OpenAIEmbeddings(openai_api_key=key)
        vectordb = Chroma.from_documents(documents=docs, embedding=openai_embeddings, persist_directory=DB_DIR)
        vectordb.persist()

        # Create retriever and model
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})
        llm = ChatOpenAI(model_name='gpt-3.5-turbo')

        # Create RetrievalQA chain
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

        # Get response
        response = qa(question)
        st.write(response)

if __name__ == '__main__':
    main()

