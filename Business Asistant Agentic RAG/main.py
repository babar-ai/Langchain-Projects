import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq 
from langchain.agents import initialize_agent
from langchain.agents import load_agent,load_tools
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.prompts.chat import (ChatPromptTemplate, HumanMessagePromptTemplate,SystemMessagePromptTemplate,MessagesPlaceholder)
from langchain.tools import BaseTool
from langchain.agents import Tool,AgentExecutor
from typing import Union
from bs4 import BeautifulSoup
import requests
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.tools.retriever import create_retriever_tool
import streamlit as st
import validators 

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

#defining a custom MATHAMATHIC tool 
class CalculatorTool(BaseTool):
    name = "CalculatorTool"
    
    description = """
    Useful for when you need to answer questions about math.
    This tool is only for math questions and nothing else.
    Formulate the input as python code.
     """

    def _run(self, question: str):
        return eval(question)
    
    def _arun(self, question: str):
     raise NotImplementedError("This tool does not support async")


def process_url(url):
    
    if not validators.url(url):
        st.error("Invalid URL. Please enter a valid URL.")
        return None

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content,'html.parser')
        page_text = soup.get_text(separator='\n')            # Extract text from the page
    
    except Exception as e:
        st.error(f"An error occurred while scraping the URL: {e}")
        return None
    
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1500, chunk_overlap=200)
    docs = text_splitter.split_text(page_text)
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_texts(docs, embedding_model)
    
    return db
    

def process_userquery(query,vector_database,chat_history):
   
    llm = ChatGroq(
      model_name = "llama-3.1-70b-versatile",
      groq_api_key = GROQ_API_KEY,
      temperature= 0
    )
    
    system_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer."""
    message = [
    SystemMessagePromptTemplate.from_template(system_template),
    MessagesPlaceholder(variable_name = "chat_history"),
    HumanMessagePromptTemplate.from_template('{input}'),
    MessagesPlaceholder(variable_name = "agent_scratchpad") ]
    
    PROMPT = ChatPromptTemplate(message)

    tools = load_tools(["ddg-search","llm-math","wikipedia"],llm=llm)

    vector_db = vector_database
    #retriver
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    
    #to make a retriver as agentic tool
    retriever_tool = create_retriever_tool(
        retriever,
        "uet_mardan_search",
        "use this tool when searching about Univesity of Engineering and Technology Mardan, khyber phukhtunkhwa Pakistan."
    )
    #to add  retriver as tool
    tools.append(retriever_tool)


# Add the custom CalculatorTool to the list of tools
    calculator_tool = CalculatorTool()
    tools.append(calculator_tool)

# Create an agent
    zero_shot_Agent = initialize_agent(
        agent="zero-shot-react-description",
        tools=tools,
        prompt=PROMPT,
        llm=llm,
        verbose=True,
        max_iterations=3
    )

    agent_Executer = AgentExecutor(
        agent = zero_shot_Agent,
        tools = tools
    )
    
    response = agent_Executer.invoke({
        "input" : "hello"
    })
    
    return response

# Main function for Streamlit app
def main():
    st.title("Your Business Assistant")
    st.header("ASK QUESTIONS")
    
    # Sidebar for URL configuration
    with st.sidebar:
        st.header("Configure URL")
        urls = st.text_area("Paste URL:")
        

        if st.button("Submit URL"):
            vector_db = process_url(urls)
            if vector_db:
                st.session_state['vector_db'] = vector_db
                st.success("URL processed and data embedded successfully.")
                st.session_state['urls_processed'] = True
            
            else:
                 st.error("Failed to process the URL. Please check the URL and try again.")

    # Ensure 'vector_db' exists in session state
    if 'vector_db' not in st.session_state:
        st.session_state['vector_db'] = None                        #session_state is an storage 

    # Create a container for chat messages
    chat_container = st.container()

    # Display the chat messages
    with chat_container:
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        # Displaying chat history
        for chat in st.session_state['chat_history']:
            st.chat_message("user").write(chat["question"])
            st.chat_message("ai").write(chat["answer"])

    # User query input fixed at the bottom
    col1, col2 = st.columns([8, 1])
    with col1:
        question = st.text_input("Ask a question:", key="user_query")
    with col2:
        if st.button("Send"):
            if question and st.session_state['vector_db']:
                chat_history = st.session_state.get("chat_history", [])
                
                # Function call
                response =process_userquery(question, st.session_state['vector_db'], chat_history)

                # Update chat history
                chat_history.append({"question": question, "answer": response['answer']})
                st.session_state['chat_history'] = chat_history

                # Display the response in the chat container
                with chat_container:
                    st.chat_message("user").write(question)
                    st.chat_message("ai").write(response['answer'])

                # Scroll to the bottom of the chat container
                st.markdown(f'<div id="bottom"></div>', unsafe_allow_html=True)
                st.markdown('<script>document.getElementById("bottom").scrollIntoView();</script>', unsafe_allow_html=True)
            else:
                st.error("Please submit a valid URL first.")
                
if __name__ == "__main__":
    main()