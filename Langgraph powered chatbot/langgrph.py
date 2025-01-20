from typing import Annotated
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq

# Define the State class
class State(BaseModel):
    """
    The State class defines the structure of the chatbot state.
    Messages have the type `list`. The `add_messages` function in the
    annotation defines how this state key should be updated.
    """
    messages: Annotated[list, add_messages]

# Create a StateGraph builder
graph_builder = StateGraph(State)

# Initialize the LLM
llm = ChatGroq(
    temperature=0,
    groq_api_key="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",
    model_name="llama-3.1-70b-versatile"
)

# Define the chatbot node function
def chatbot(state: State):
    """
    The chatbot node function processes the current state and generates
    a response using the LLM.
    """
    return {"messages": [llm.invoke(state.messages)]}

# Add the chatbot node to the graph
graph_builder.add_node("chatbot", chatbot)

# Define edges to specify the flow of the graph
graph_builder.add_edge(START, "chatbot")  # Start at the chatbot node
graph_builder.add_edge("chatbot", END)   # End after chatbot node execution

# Compile the graph
graph = graph_builder.compile()

# Main loop for the chatbot
if __name__ == "__main__":
    print("Chatbot initialized. Type 'quit', 'exit', or 'q' to end the conversation.")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        # Stream responses from the graph
        for event in graph.stream({"messages": [("user", user_input)]}):
            for value in event.values():
                print("Assistant:", value["messages"][-1].content)
