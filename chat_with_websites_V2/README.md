# 🦜🔗 Chat With Websites

## Overview

"Chat With Websites" is a powerful tool designed to scrape website content, process natural language queries, and provide intelligent responses using state-of-the-art machine learning techniques. This application is built with **Streamlit** for the user interface and leverages technologies like **LangChain**, **FAISS**, and **ChatGroq LLM** to analyze and interact with data effectively.

---

## Features

### 🔗 URL Content Scraping
- Input a URL to extract its content.
- Automatically detects and solves CAPTCHA challenges.

### 🤖 AI-Powered Q&A
- Use natural language to ask questions about the content of a webpage.
- Powered by ChatGroq LLM and LangChain for accurate and relevant answers.

### 📂 Interactive Data Analysis
- Upload CSV files to analyze datasets interactively.
- Supports natural language queries and provides concise insights.

### 🛠️ Streamlined User Experience
- Clean and intuitive interface built with Streamlit.
- Real-time chat feature with dynamic question-and-answer flow.

---

## What's New in This Version

- **Enhanced CAPTCHA Handling**: Improved CAPTCHA detection and solving for smoother web scraping.
- **Dynamic Chat Interface**: Added a scrollable chat history to maintain context across multiple queries.
- **Improved Query Processing**: Optimized natural language query handling with better accuracy and response time.
- **Advanced Visualization Support**: Enhanced integration with matplotlib for more insightful visualizations.
- **Refined Embedding Model**: Transitioned to HuggingFace's "all-MiniLM-L6-v2" for more precise vector embeddings.

---

## Technologies Used

### Programming Languages
- **Python**: Core development language.

### Libraries and Tools
- **Streamlit**: For building the interactive user interface.
- **LangChain**: Provides retrieval-based AI and conversational capabilities.
- **FAISS**: For efficient vector-based search.
- **ChatGroq**: The language model backend for processing queries.
- **Selenium**: For handling CAPTCHA and web automation.
- **BeautifulSoup**: For web scraping.
- **HuggingFace Embeddings**: For creating vector embeddings from textual data.

---

## Prerequisites

1. **Install Python**: Version 3.8 or higher is recommended.
2. **Install Dependencies**: Use the following command to install required libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Key**: Create a `.env` file in the project directory with the following content:

   ```plaintext
   GROQ_API_KEY=your_api_key_here
   ```

   Replace `your_api_key_here` with your actual API key for ChatGroq.

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

3. **Start the Application**:
   ```bash
   streamlit run main.py
   ```

4. **Access the App**:
   Open your browser and navigate to `http://localhost:8501` to interact with the application.

---

## Example Use Case

1. **Upload a CSV File**:
   - Upload a file like `sales_data.csv` in the provided section.
   - The app displays the first few rows for a quick overview.

2. **Ask Questions**:
   - Example queries:
     - "What are the top 5 products by revenue?"
     - "Show me a graph of monthly sales trends."

3. **Process Website Content**:
   - Paste a URL to scrape the content and ask questions like:
     - "What are the key topics covered on this page?"
     - "Summarize the main points of the article."

4. **Interactive Responses**:
   - Receive concise answers and insights in real time.
   - Visualize trends and statistics based on the data.

---

## Folder Structure

```plaintext
📂 Project Directory
├── main.py                # Main application script
├── requirements.txt       # Required Python libraries
├── .env                   # Environment variables (API key)
├── README.md              # Project documentation
```

---

## Acknowledgments

This project is built with the support of several open-source tools and libraries:

- **Streamlit**: For creating a dynamic user interface.
- **LangChain**: For retrieval-augmented AI capabilities.
- **ChatGroq**: For state-of-the-art language processing.
- **FAISS**: For efficient vector search operations.
- **Selenium and BeautifulSoup**: For robust web scraping.

Special thanks to the developers of these technologies for their contributions to open-source software.

---

## License

This project is licensed under the MIT License.
