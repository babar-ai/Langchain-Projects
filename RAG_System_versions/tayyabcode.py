import os
import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import FireCrawlLoader
from langchain.docstore.document import Document
from langchain.vectorstores.faiss import FAISS
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha
import os

# Define system template
system_template = """Use the following pieces of context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
"""

# Load environment variables
# load_dotenv()

# Define message templates
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]

os.environ["GOOGLE_API_KEY"] = "AIzaSyCMtgjCDQl7iBJsLa2iGTH0KBmsIw3UGFo"

# Create chat prompt template
prompt = ChatPromptTemplate.from_messages(messages)

# Define constants
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(ABS_PATH, "db")

### Use this on line 82 only if you have 2captcha api key coz its paidddd
def bypass_captcha(url):
    browser = webdriver.Chrome()
    browser.get('https://2captcha.com/demo/normal')

    captcha_img = browser.find_element(By.CLASS_NAME, '_17bwEOs9gv8ZKqqYcEnMuQ') # Provide the class name of the image
    captcha_img.screenshot('captchas/captcha.png')

    api_key = os.getenv('APIKEY_2CAPTCHA', '') # Put your api key in here from 2captcha

    solver = TwoCaptcha(api_key)

    try:
        result = solver.normal('captchas/captcha.png')

    except Exception as e:
        print(e)

    else:
        code = result['code']

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'simple-captcha-field'))) # Put input field id in here 

        browser.find_element(By.ID, 'simple-captcha-field').send_keys(code) # Put input field id in here

        browser.find_element(By.CLASS_NAME, "button-primary").click() # It can be change. Look for this one too

        browser.find_element(By.XPATH, '//*[@id="root"]/div/main/div/section/form/button[1]').click() # Find button and copy its xpath


# Function to process URLs
def process_urls(urls):
    url_list = [url.strip() for url in urls.split(",")]
    all_docs = []

    for url in url_list:
        ## Uncomment this line if you have api key of 2captcha
        # bypass_captcha(url) 
        loader = FireCrawlLoader(url=url, mode="crawl", api_key='fc-388f07deeea146a298d11101a40343eb')
        data = loader.load()

        # Split the loaded data
        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=512, chunk_overlap=100)
        docs = text_splitter.split_documents(data)
        all_docs.extend(docs)

    # Filter documents
    filtered_docs = []
    for doc in all_docs:
        if isinstance(doc, Document) and hasattr(doc, "metadata"):
            clean_metadata = {
                k: v
                for k, v in doc.metadata.items()
                if isinstance(v, (str, int, float, bool))
            }
            filtered_docs.append(Document(page_content=doc.page_content, metadata=clean_metadata))

    # Initialize embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Create a FAISS vector database from the documents
    vectordb = FAISS.from_documents(documents=filtered_docs, embedding=embeddings)
    vectordb.save_local(DB_DIR)

    return vectordb

# Function to process query
def process_query(vectordb, query, chat_history):
    # Create a retriever from the FAISS vector database
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    # Use a Llama3-70b model
    llm = ChatGroq(
        api_key="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",
        temperature=0,
        model="llama3-70b-8192",
    )

    # Create a ConversationalRetrievalChain with a StuffedDocumentChain
    chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff",
        verbose=True,
    )

    # Format chat history to a list of tuples
    formatted_chat_history = [(item['question'], item['answer']) for item in chat_history]

    # Run the prompt and return the response
    response = chain({"question": query, "chat_history": formatted_chat_history})

    return response

def main():
    # Set the title and subtitle of the app
    st.title("🦜🔗 Chat With Websites")
    st.header("Ask Questions")
    query = st.text_input("Ask a question (query/prompt)")

    # Sidebar for URL input
    with st.sidebar:
        st.header("Configure URLs")
        urls = st.text_area("Insert the website URLs (comma-separated)")
        if st.button("Submit URLs"):
            vectordb = process_urls(urls)
            st.session_state['vectordb'] = vectordb
            st.success("URLs processed and data embedded successfully.")
            st.session_state['urls_processed'] = True

    # Main area for query input and responses
    if 'urls_processed' in st.session_state and st.session_state['urls_processed']:
        if st.button("Submit Query", key="query_submit"):
            chat_history = st.session_state.get('chat_history', [])
            response = process_query(st.session_state['vectordb'], query, chat_history)
            st.write(response["answer"])
            chat_history.append({"question": query, "answer": response["answer"]})
            st.session_state['chat_history'] = chat_history

if __name__ == "__main__":
    main()
