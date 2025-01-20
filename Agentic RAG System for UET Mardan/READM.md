# 🌐 LangChain Agents for UET Mardan

## Overview

This project implements an AI-powered agent designed to assist prospective students in making informed decisions about enrolling at the University of Engineering and Technology (UET) Mardan. It uses **LangChain** and **ChatGroq LLM** to provide accurate, conversational responses about university programs, admissions, and other details. The application also includes web scraping and information retrieval capabilities to generate precise and dynamic responses.

---

## Features

### 🤖 AI-Powered Assistance
- Uses the **ChatGroq LLM** to handle natural language queries with context-aware answers.
- Provides personalized guidance tailored for prospective students and parents.

### 🌐 Web Scraping
- Scrapes UET Mardan's website to collect detailed information about programs, admissions, and events.
- Automatically extracts and processes internal links to ensure comprehensive coverage.

### 🔍 Information Retrieval
- Processes scraped website data into vector embeddings using **FAISS** and **HuggingFace Embeddings**.
- Allows efficient and accurate information retrieval through a retriever tool.

### 🛠️ Zero-Shot Agent
- Integrates additional tools like DuckDuckGo Search, Wikipedia, and math capabilities to enhance the AI's utility.
- Configured with a salesperson persona for persuasive and user-friendly interaction.

---

## Technologies Used

### Programming Languages
- **Python**

### Libraries and Frameworks
- **LangChain**: Core framework for conversational AI.
- **ChatGroq LLM**: Backend language model for natural language understanding.
- **FAISS**: Vector-based similarity search for efficient information retrieval.
- **HuggingFace Embeddings**: Creates document embeddings for retrieval.
- **BeautifulSoup**: Web scraping for content extraction.
- **Requests**: For making HTTP requests.

---

## How It Works

1. **Scraping the Website**:
   - Starts with a specified URL (e.g., UET Mardan's homepage).
   - Extracts text and internal links from the pages.
   - Limits scraping to 100 pages to balance performance and data coverage.

2. **Processing Data**:
   - Splits extracted content into chunks for efficient processing.
   - Converts chunks into embeddings using **HuggingFace's MiniLM-L6-v2** model.
   - Stores embeddings in **FAISS** for similarity-based retrieval.

3. **Query Handling**:
   - Uses the **ChatGroq LLM** to process natural language queries.
   - Retrieves relevant information from the vector database and other tools.

4. **Agent Interaction**:
   - Responds to user queries with contextual, accurate, and persuasive answers.
   - Highlights UET Mardan's unique features and advantages for potential students.

---

## Prerequisites

1. **Install Python**: Ensure Python 3.8 or higher is installed.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
