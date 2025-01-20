# 🤖 LangGraph-Powered Chatbot

## Overview

This project implements a chatbot using **LangGraph** and **ChatGroq**. It defines the chatbot as a state machine, enabling efficient handling of user queries and responses. The project uses **LangGraph's StateGraph** to structure the chatbot workflow, where each node represents a processing step.

---

## Features

### 🛠️ State Machine Design
- Structured as a state graph using **LangGraph**.
- Ensures clear and maintainable chatbot flow through well-defined nodes and edges.

### 🤖 AI-Powered Responses
- Powered by **ChatGroq LLM** for natural language processing and response generation.
- Provides accurate and context-aware responses.

### 🔄 Real-Time Interaction
- Continuously listens for user input and responds interactively.
- Allows users to end the conversation with commands like `quit`, `exit`, or `q`.

---

## How It Works

1. **StateGraph Setup**:
   - Defines the chatbot's state using the `State` class.
   - Messages are stored and updated dynamically using LangGraph's `add_messages` function.

2. **Chatbot Node**:
   - Handles user input and generates responses using ChatGroq LLM.
   - Updates the state with new messages.

3. **Graph Workflow**:
   - The graph starts at the `chatbot` node and ends after processing the user query.

4. **Interactive Loop**:
   - Users interact with the chatbot in a continuous loop until they decide to exit.

---

## Technologies Used

### Programming Languages
- **Python**

### Libraries and Tools
- **LangGraph**: For defining and managing the chatbot's state graph.
- **ChatGroq**: Large language model for generating responses.
- **Pydantic**: For data validation and parsing.

---

## Prerequisites

1. **Install Python**:
   - Ensure Python 3.8 or higher is installed on your system.

2. **Install Dependencies**:
   - Install the required libraries using:
     ```bash
     pip install -r requirements.txt
     ```

3. **Set Up API Keys**:
   - Create a `.env` file in the project directory and add your ChatGroq API key:
     ```plaintext
     GROQ_API_KEY=your_api_key_here
     ```

---

## Running the Chatbot

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Chatbot**:
   ```bash
   python langgraph_00.py
   ```

4. **Interact with the Chatbot**:
   - Input your queries, and the chatbot will provide responses.
   - Exit the chatbot by typing `quit`, `exit`, or `q`.

---

## Example Interaction

```plaintext
User: Hello, chatbot!
Assistant: Hi there! How can I assist you today?

User: Tell me about LangGraph.
Assistant: LangGraph is a framework for building state-machine-based workflows in Python. Thanks for asking!

User: quit
Goodbye!
```

---

## Folder Structure

```plaintext
📂 Project Directory
├── langgraph_00.py        # Main chatbot script
├── requirements.txt       # Required libraries
├── .env                   # API keys for external tools
├── README.md              # Project documentation
```

---

## Acknowledgments

Special thanks to the developers of:
- **LangGraph**: For providing a structured framework for building state machines.
- **ChatGroq**: For delivering advanced language model capabilities.

---

## License

This project is licensed under the MIT License.
