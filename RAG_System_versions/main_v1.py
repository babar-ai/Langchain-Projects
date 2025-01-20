# chatbot with authentication 

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from amazoncaptcha import AmazonCaptcha
from bs4 import BeautifulSoup
import requests
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.chat import (ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
from langchain_groq import ChatGroq
import time
from langchain_core.messages import HumanMessage, AIMessage

# In-memory storage for user credentials (for demo purposes)
user_credentials = {}

# Template for the conversation
system_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer."""

message = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template('{input}'),
] 

PROMPT = ChatPromptTemplate(message)

def detect_and_solve_captcha(driver):
    try:
        captcha_image_element = driver.find_element(By.XPATH, "//img[contains(@src, 'captcha')]")
        captcha_image_url = captcha_image_element.get_attribute('src')
        if captcha_image_url:
            captcha = AmazonCaptcha.fromlink(captcha_image_url)
            captcha_value = AmazonCaptcha.solve(captcha)

            input_field = driver.find_element(By.ID, "captchacharacters")
            input_field.send_keys(captcha_value)

            button = driver.find_element(By.CLASS_NAME, "a-button-text")
            button.click()
            return True
        
    except Exception as e:
        st.error(f"Error detecting or solving CAPTCHA: {e}")
    return False

def Process_urls(url, chrome_driver_path=None):
    try:
        if chrome_driver_path:
            options = Options()
            options.add_argument("--headless")
            service = Service(chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=options)

            driver.get(url)

            if detect_and_solve_captcha(driver):
                st.info("CAPTCHA detected and solved. Reloading page...")
                time.sleep(5)
                driver.get(url)

            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            captcha_image = soup.find('img', src=True, alt='Captcha')
            if captcha_image:
                st.error("CAPTCHA detected. Please solve it manually.")
                return None

            data = soup.get_text(separator='\n')
            text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1500, chunk_overlap=200)
            docs = text_splitter.split_text(data)
            embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            db = FAISS.from_texts(docs, embedding_model)
            return db
        else:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            data = soup.get_text(separator='\n')
            text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1500, chunk_overlap=200)
            docs = text_splitter.split_text(data)
            embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            db = FAISS.from_texts(docs, embedding_model)
            return db
    except requests.RequestException as e:
        st.error(f"Error fetching data from website: {e}")
        return None
    except Exception as e:
        st.error(f"Error processing URL: {e}")
        return None

def process_user_query(question, vector_db, chat_history):
    llm = ChatGroq(
        temperature=0,
        groq_api_key="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",
        model_name="llama-3.1-70b-versatile"
    )
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        verbose=True,
        return_source_documents=True,
        chain_type='stuff'
    )

    formatted_chat_history = [(item['question'], item['answer']) for item in chat_history]

    response = chain({"question": question, "chat_history": formatted_chat_history})
    return response


import json
import os

# File to store user credentials
CREDENTIALS_FILE = "user_credentials.json"

# Load user credentials from file
def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return {}  # Return an empty dictionary if file doesn't exist

# Save user credentials to file
def save_credentials(credentials):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file)

# Initialize user credentials
user_credentials = load_credentials()

def authenticate_user():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False  # Initialize authenticated state

    st.sidebar.header("User Authentication")
    auth_choice = st.sidebar.radio("Select an option:", ["Login", "Register"], index=0)

    if auth_choice == "Login":
        username = st.sidebar.text_input("Username", key="login_username")
        password = st.sidebar.text_input("Password", type="password", key="login_password")
        if st.sidebar.button("Login"):
            if username in user_credentials and user_credentials[username] == password:
                st.session_state['authenticated'] = True  # Update session state
                st.sidebar.success("Logged in successfully!")
                return True
            else:
                st.sidebar.error("Invalid credentials. Please try again.")
                return False

    elif auth_choice == "Register":
        new_username = st.sidebar.text_input("New Username", key="register_username")
        new_password = st.sidebar.text_input("New Password", type="password", key="register_password")
        if st.sidebar.button("Register"):
            if new_username in user_credentials:
                st.sidebar.error("Username already exists. Please choose a different username.")
                return False
            else:
                user_credentials[new_username] = new_password  # Add new user to the dictionary
                save_credentials(user_credentials)  # Save the updated credentials to the file
                st.sidebar.success("Registration successful. Please log in.")
                return False

    return st.session_state['authenticated']




def main():
    st.title("🦜🔗 Chat With Websites")

    # Ensure session state for authentication is set
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    # Handle authentication
    if not st.session_state['authenticated']:
        authenticated = authenticate_user()
        if not authenticated:
            st.warning("Please log in to access the app.")
            return  # Stop execution until the user logs in

    # Main app content after successful login
    st.header("Welcome to the Chatbot Application!")
    st.write("You are now logged in and can access the app features.")

    # Example application content
    st.text("This is the main application.")
    # Add your chatbot or app content here...

    
    with st.sidebar:
        st.header("Configure URL")
        urls = st.text_area("Paste URL:")
        chrome_driver_path = st.text_input("Path to ChromeDriver (optional)", "")

        if st.button("Submit URL"):
            vector_db = Process_urls(urls, chrome_driver_path)
            if vector_db:
                st.session_state['vector_db'] = vector_db
                st.success("URL processed and data embedded successfully.")
                st.session_state['urls_processed'] = True

    if 'vector_db' not in st.session_state:
        st.session_state['vector_db'] = None

    chat_container = st.container()

    with chat_container:
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        for chat in st.session_state['chat_history']:
            st.chat_message("user").write(chat["question"])
            st.chat_message("ai").write(chat["answer"])

    col1, col2 = st.columns([8, 1])
    with col1:
        question = st.text_input("Ask a question:", key="user_query")
    with col2:
        if st.button("Send"):
            if question and st.session_state['vector_db']:
                chat_history = st.session_state.get("chat_history", [])
                response = process_user_query(question, st.session_state['vector_db'], chat_history)

                chat_history.append({"question": question, "answer": response['answer']})
                st.session_state['chat_history'] = chat_history

                with chat_container:
                    st.chat_message("user").write(question)
                    st.chat_message("ai").write(response['answer'])

if __name__ == "__main__":
    main()


