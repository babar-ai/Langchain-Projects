
from langchain.prompts.chat import (ChatPromptTemplate, HumanMessagePromptTemplate,SystemMessagePromptTemplate,MessagesPlaceholder)
from typing import Union
from typing import Optional
import streamlit as st
from helper_funtion import process_url, text_splitter, create_vector_db, get_llm, retriever, zero_shot_agent
from lc_tools import retriever_tool, all_tools



# PROMPT = ChatPromptTemplate(
#     messages = [
# ("system", "Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say thanks for asking! at the end of the answer."),
# MessagesPlaceholder(variable_name = "chat_history"),
# HumanMessagePromptTemplate.from_template('{input}'),
# MessagesPlaceholder(variable_name = "agent_scratchpad") ]
# )



# Main function for Streamlit app
def main():
    st.title("your virtual assistant")
    st.header("ASK QUESTIONS ABOUT UET MARDAN")
    
    # Sidebar for URL configuration
    with st.sidebar:
        st.header("Configure URL")
        urls = st.text_area("Paste URL:")
        

        if st.button("Submit URL"):
            text_data = process_url(urls)
            
            if text_data:
                docs = text_splitter(text_data)
                vector_db = create_vector_db(docs)

                # Store the vector database in session state
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
                retriever = st.session_state['vector_db'].as_retriever(search_kwargs={"k": 3})
                llm = get_llm()
                Retriever_tool = retriever_tool(retriever)
                tools = all_tools(llm, retriever_tool)

                # Function call
                response = zero_shot_agent(tools, llm, PROMPT, question)
                # response =process_userquery(question, st.session_state['vector_db'], chat_history)

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