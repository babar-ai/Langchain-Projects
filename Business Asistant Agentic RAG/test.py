from helper_funtion import process_url, text_splitter, create_vector_db, get_llm, retriever, zero_shot_agent
from langchain.prompts.chat import (ChatPromptTemplate, HumanMessagePromptTemplate,SystemMessagePromptTemplate,MessagesPlaceholder)
from lc_tools import retriever_tool, all_tools
from main import PROMPT
 

prompts = PROMPT

url = process_url("https://www.uetmardan.edu.pk/")
docs = text_splitter(url)
vector_db = create_vector_db(docs)  
retriever = retriever(vector_db)
llm = get_llm() 
retriever_tool = retriever_tool(retriever)
tools = all_tools(llm,retriever_tool)   
question = "What is the mission of UET Mardan?"
response = zero_shot_agent(tools, llm, question)
print(response)

