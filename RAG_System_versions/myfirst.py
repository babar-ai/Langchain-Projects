import os
from lark import Lark, Transformer
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chains import ConversationChain
'''
The ConversationChain is typically used when you want a simple conversation flow without the need to retrieve external information or interact with 
external APIs. It works directly with the 
language model to generate responses based on the conversation history.
'''
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from bs4 import BeautifulSoup
import requests
import streamlit as st
from pyngrok import ngrok
from langchain_groq import ChatGroq

url = "https://uetmardan.edu.pk/"
response = requests.get(url)

if response.status_code == 200:
        # Define soup object
        soup = BeautifulSoup(response.content, 'html.parser')
        data = soup.get_text(separator="\n")
        # 'data' is class<str>
else:
    print("Error while fetching data from website")
      

    # Split the Document
text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1500,
        chunk_overlap=200
)
docs = text_splitter.split_text(data)

    # Embed the Split Text
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Vector Store (Facebook AI Similarity Search (Faiss))
db = FAISS.from_texts(
        docs,
        embedding_model
)

    # LLM
llm = ChatGroq(
        temperature=0,
        groq_api_key="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",
        model_name="llama-3.1-70b-versatile"
)

template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.

Current conversation:
{history}
Human: {input}
AI Assistant:"""

PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

memory = ConversationBufferMemory(ai_prefix="AI Assistant")

    # ConversationChain
chain = ConversationChain(
        llm=llm,
        prompt=PROMPT,
        memory=memory,
        verbose=True
)

    # Get response from the conversation chain
query="where is uet mardan located"
response = chain.run(input=query)
print("Initial Memory Content:", memory.chat_memory.messages)
print(response)
query1 = "how many departments are there"
response = chain.run(input=query1)
print(response)
print("Memory Content After Query:", memory.chat_memory.messages)





