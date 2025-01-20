# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from amazoncaptcha import AmazonCaptcha

# # Define the path to your ChromeDriver
# #chome>setting>help
# chrome_driver_path = r"chromedriver-win64\chromedriver.exe"

# def solving_captcha(driver_path,url):
# # Initialize the Service object
#     service = Service(chrome_driver_path)

# # Add options to keep the browser open
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option("detach", True)

# # Initialize the Chrome driver with the Service object and options
#     driver = webdriver.Chrome(service=service, options=options)

# # Open the Amazon captcha validation page
#     driver.get("https://www.amazon.com/errors/validateCaptcha")
#     link = driver.find_element(By.XPATH,"//div[@class = 'a-row a-text-center']//img").get_attribute('src')

#     captcha = AmazonCaptcha.fromlink(link)
#     captcha_value = AmazonCaptcha.solve(captcha)

#     input_field = driver.find_element(By.ID,"captchacharacters").send_keys(captcha_value)
# #button
#     button = driver.find_element(By.CLASS_NAME, "a-button-text")
#     button.click()


# import streamlit as st
# from bs4 import BeautifulSoup
# import requests
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.chains import RetrievalQA
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq
# from pyngrok import ngrok
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from amazoncaptcha import AmazonCaptcha

# # Function to handle Amazon CAPTCHA
# def handle_amazon_captcha(chrome_driver_path):
#     # Initialize the Service object
#     service = Service(chrome_driver_path)

#     # Add options to keep the browser open
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option("detach", True)

#     # Initialize the Chrome driver with the Service object and options
#     driver = webdriver.Chrome(service=service, options=options)

#     # Open the Amazon captcha validation page
#     driver.get("https://www.amazon.com/errors/validateCaptcha")
#     link = driver.find_element(By.XPATH, "//div[@class = 'a-row a-text-center']//img").get_attribute('src')

#     captcha = AmazonCaptcha.fromlink(link)
#     captcha_value = AmazonCaptcha.solve(captcha)

#     input_field = driver.find_element(By.ID, "captchacharacters").send_keys(captcha_value)
    
#     # Click the button to submit the CAPTCHA
#     button = driver.find_element(By.CLASS_NAME, "a-button-text")
#     button.click()
    
#     return driver

# def Process_url(url, chrome_driver_path=None):
#     # Handle CAPTCHA if ChromeDriver path is provided
#     if chrome_driver_path:
#         handle_amazon_captcha(chrome_driver_path)
#         st.success("Amazon CAPTCHA handled successfully.")
#     else:
#         print("somthing went wrong while solving captcha")

#     # Process the URL
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         data = soup.get_text(separator='\n')
#         text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1500, chunk_overlap=200)
#         docs = text_splitter.split_text(data)
#         embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#         db = FAISS.from_texts(docs, embedding_model)
#         return db
#     else:
#         st.error("Error while fetching data from website")

# def main():
#     # CSS for styling the chat interface
#     st.markdown("""
#         <style>
#         body {
#             background-color: #F0F0F0; /* Light gray background */
#             color: #333333; /* Dark gray text for readability */
#         }
#         .output-box {
#             background-color: #ffffff; /* White background for output box */
#             border: 2px solid #000000; /* Black outline */
#             border-radius: 8px;
#             padding: 15px;
#             margin-top: 10px;
#             color: #333333; /* Dark gray text */
#             box-shadow: 0 0 15px rgba(0, 0, 0, 0.3); /* Glow effect */
#             display: flex;
#             align-items: center;
#         }
#         .output-box i {
#             font-size: 24px;
#             margin-right: 10px;
#         }
#         .sidebar .sidebar-content {
#             background-color: #E0E0E0; /* Slightly darker gray for sidebar */
#         }
#         </style>
#         <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
#     """, unsafe_allow_html=True)

#     st.title("🦜🔗 Chat With Websites")
#     st.header("ASK QUESTIONS")

#     if 'vector_db' not in st.session_state:
#         st.session_state['vector_db'] = None

#     query = st.text_input("Ask a question:")

#     if query and st.session_state['vector_db']:
#         llm = ChatGroq(
#             temperature=0,
#             groq_api_key="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",
#             model_name="llama-3.1-70b-versatile"
#         )

#         template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
#         {context}
#         Question: {question}
#         Helpful Answer: """
#         QA_CHAIN_PROMPT = ChatPromptTemplate.from_template(template)

#         qa_chain = RetrievalQA.from_chain_type(
#             llm,
#             chain_type="stuff",
#             retriever=st.session_state['vector_db'].as_retriever(),
#             return_source_documents=True,
#             chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
#         )

#         result = qa_chain({"query": query})
#         st.markdown(f'<div class="output-box"><i class="fas fa-robot"></i>{result["result"]}</div>', unsafe_allow_html=True)

#     with st.sidebar:
#         st.header("Configure URL")
#         url = st.text_area("Paste URL")
#         chrome_driver_path = st.text_input("Optional: ChromeDriver Path", value="")

#         if st.button("Submit URL"):
#             vector_db = Process_url(url, chrome_driver_path if chrome_driver_path else None)
#             if vector_db:
#                 st.session_state['vector_db'] = vector_db
#                 st.success("URL processed and data embedded successfully.")
#                 st.session_state['url_processed'] = True

# if __name__ == "__main__":
#     main()







import streamlit as st
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from amazoncaptcha import AmazonCaptcha
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import time

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

def Process_url(url, chrome_driver_path=None):
    try:
        if chrome_driver_path:
            options = Options()
            options.add_argument("--headless")  # Optional: Run in headless mode
            service = Service(chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=options)

            driver.get(url)

            # Check if CAPTCHA is present and solve it
            if detect_and_solve_captcha(driver):
                st.info("CAPTCHA detected and solved. Reloading page...")
                time.sleep(5)  # Wait for the page to reload
                driver.get(url)
            
            # Continue fetching page content if CAPTCHA solved or not present
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

def main():
    st.markdown("""
        <style>
        body {
            background-color: #F0F0F0;
            color: #333333;
        }
        .output-box {
            background-color: #ffffff;
            border: 2px solid #000000;
            border-radius: 8px;
            padding: 15px;
            margin-top: 10px;
            color: #333333;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
            display: flex;
            align-items: center;
        }
        .output-box i {
            font-size: 24px;
            margin-right: 10px;
        }
        .sidebar .sidebar-content {
            background-color: #E0E0E0;
        }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True)

    st.title("🦜🔗 Chat With Websites")
    st.header("ASK QUESTIONS")

    if 'vector_db' not in st.session_state:
        st.session_state['vector_db'] = None

    query = st.text_input("Ask a question:")

    if query and st.session_state['vector_db']:
        llm = ChatGroq(
            temperature=0,
            groq_api_key="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",
            model_name="llama-3.1-70b-versatile"
        )

        template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
        {context}
        Question: {question}
        Helpful Answer: """
        QA_CHAIN_PROMPT = ChatPromptTemplate.from_template(template)

        qa_chain = RetrievalQA.from_chain_type(
            llm,
            chain_type="stuff",
            retriever=st.session_state['vector_db'].as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )

        result = qa_chain({"query": query})
        st.markdown(f'<div class="output-box"><i class="fas fa-robot"></i>{result["result"]}</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.header("Configure URL")
        url = st.text_area("Paste URL")
        chrome_driver_path = st.text_input("Path to ChromeDriver (optional)", "")

        if st.button("Submit URL"):
            vector_db = Process_url(url, chrome_driver_path)
            if vector_db:
                st.session_state['vector_db'] = vector_db
                st.success("URL processed and data embedded successfully.")
                st.session_state['url_processed'] = True

if __name__ == "__main__":
    main()
