# 🤖 Your Business Assistant

## Overview

This project is an AI-powered assistant designed to handle complex queries about your business or a specific website. It processes URLs to extract and embed relevant information, integrates tools for math calculations, and provides dynamic conversational responses through a powerful language model.

---

## Features

### 🌐 URL Content Processing
- Scrapes webpage content and transforms it into a searchable vector database.
- Supports dynamic content embedding using **HuggingFace Embeddings** and **FAISS**.

### 🤖 Conversational Query Handling
- Uses **ChatGroq** to provide context-aware, concise responses.
- Dynamically loads tools like DuckDuckGo, Wikipedia, and a custom calculator for advanced query handling.

### 🛠️ Tool Integration
- Includes:
  - **Math Calculation Tool**: Solves math-related queries.
  - **Retriever Tool**: Queries processed web content for insights.
  - External tools like **Wikipedia Search** and **DuckDuckGo**.

### 💬 Streamlit Interface
- Provides an interactive UI for entering URLs and queries.
- Maintains session-based chat history for continuous conversations.

---

## Technologies Used

### Programming Languages
- **Python**

### Libraries and Tools
- **Streamlit**: For the user interface.
- **LangChain**: Core framework for query handling and memory.
- **ChatGroq**: Language model for natural language understanding.
- **BeautifulSoup**: For web scraping.
- **FAISS**: Vector-based similarity search.
- **HuggingFace Embeddings**: For embedding textual data.

---

## Prerequisites

1. **Install Python**:
   - Ensure Python 3.8 or higher is installed.

2. **Install Dependencies**:
   - Install required libraries using:
     ```bash
     pip install -r requirements.txt
     ```

3. **Set Up API Keys**:
   - Create a `.env` file in the project directory and include your API keys:
     ```plaintext
     GROQ_API_KEY=your_groq_api_key_here
     TAVILY_API_KEY=your_tavily_api_key_here
     ```

---

## Running the Application

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run main.py
   ```

4. **Interact with the Assistant**:
   - Paste a URL to process content.
   - Input your queries to receive insightful responses.

---

## Example Interaction

**Step 1**: Paste a valid URL in the sidebar and submit it.  
**Step 2**: Ask a question like:
- "What is the main topic of this webpage?"
- "Summarize the admissions process for UET Mardan."

**Step 3**: Receive dynamic, AI-powered responses:
- "The webpage focuses on engineering programs offered by UET Mardan. Thanks for asking!"

---

## Folder Structure

```plaintext
📂 Project Directory
├── main.py                # Main application script
├── requirements.txt       # Required dependencies
├── .env                   # API keys configuration
├── README.md              # Project documentation
```

---

## Acknowledgments

Special thanks to:
- **LangChain**: For enabling tool and memory integration.
- **ChatGroq**: For delivering advanced language processing capabilities.
- **BeautifulSoup**: For simplifying web scraping.

---

## License

This project is licensed under the MIT License.
