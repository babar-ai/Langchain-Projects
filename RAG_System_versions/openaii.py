import os 
from constants import openai_key
from langchain.llms import OpenAI 
import streamlit as st

os.environ["OPENAI_API_KEY"] = openai_key

st.title("langchain Demonstration with openai API")
input_text = st.text_input("search the topic you want")

#OPENAI llm
llm = OpenAI(temprature = 0.8)
'''
In the context of language models like OpenAI's, "temperature" is a hyperparameter that controls the randomness of the model's output. 
It influences the probability distribution over the possible next words.
In the above example, temprature = 0.8 means the model will produce responses with a good balance between 
creativity and coherence, allowing for more diverse and interesting outputs while maintaining some level of structure.
'''

if input_text:
    st.write(llm(input_text))