# from langchain.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq
# from langchain.schema import HumanMessage, SystemMessage, AIMessage
# from dotenv import load_dotenv
# import os 

# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "you are helpfull websearch assistant. you will helps to find construction plan PDFs"),
#         ("human", "{user_input}"),
#     ]
# )

# chat_prompt = prompt.format_messages(user_input = "i need construction plan room pdfs")

# llm = ChatGroq(
#     model="mixtral-8x7b-32768",
#     temperature=0.0,
#     max_retries=2,
#     GROQ_API_KEY = GROQ_API_KEY
# )
