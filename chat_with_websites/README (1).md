# 🦜🔗 Chat With Websites

## Overview

"Chat With Websites" is a powerful Streamlit-based application that allows users to interactively explore website content and CSV datasets. By leveraging cutting-edge AI technologies such as ChatGroq LLM, FAISS vector embeddings, and LangChain, the app provides prompt-driven insights, scrapes web content, and processes data queries seamlessly.

---

## Key Features

### 🔗 Web Content Analysis
- Paste a URL to scrape and process the website content.
- Automatically detects and solves CAPTCHA challenges for smooth processing.

### 📊 Data Analysis with CSV Files
- Upload CSV files and explore datasets with natural language queries.
- Get detailed textual answers and visualizations without writing code.

### 🤖 Conversational AI
- Employs LangChain and ChatGroq LLM for conversational query handling.
- Provides concise, context-aware answers tailored to your questions.

### 🛠️ Interactive User Interface
- Built with Streamlit for a clean and intuitive user experience.
- Dynamic chat interface with scrollable chat history.

---

## Technologies Used

### Programming Languages
- **Python**: Core language for development.

### Libraries and Frameworks
- **Streamlit**: For the interactive user interface.
- **Selenium**: To handle CAPTCHA and web automation.
- **BeautifulSoup**: For web scraping.
- **LangChain**: For retrieval-based AI and conversational pipelines.
- **FAISS**: For vector-based similarity search.
- **ChatGroq**: For advanced LLM capabilities.
- **Pandas**: For data manipulation.
- **matplotlib**: For creating visualizations.

### Environment Management
- **dotenv**: For secure API key management.

---

## Prerequisites

### Environment Setup
- Install Python 3.8 or higher.
- Install required dependencies using:

```bash
pip install -r requirements.txt
```

### API Key
- Obtain the **ChatGroq API Key** and add it to a `.env` file:

```plaintext
GROQ_API_KEY=your_api_key_here
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

3. **Start the Application**:
   ```bash
   streamlit run main.py
   ```

4. **Access the App**:
   Open your browser and navigate to `http://localhost:8501`.

---

## Example Use Case

1. **Upload a Dataset**:
   - Open the application and upload a CSV file (e.g., `sales_data.csv`) using the file uploader in the Streamlit sidebar.

2. **Process Website Content**:
   - Paste a URL in the "Configure URL" section to extract and process the webpage content.
   - Automatically handle CAPTCHA challenges during the scraping process.

3. **Ask Questions**:
   - Input natural language queries in the chat section, such as:
     - "What are the most frequently mentioned topics on this page?"
     - "List the top 3 headlines on the page."

4. **Get AI-Powered Responses**:
   - Receive concise, text-based answers with references to the source text.
   - View visualizations and insights tailored to your queries.

---

## Folder Structure

```plaintext
📂 Project Directory
├── main.py                # Main Streamlit application
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
├── README.md              # Project documentation
```

---

## Acknowledgments

This project was made possible with the help of the following tools and libraries:

- **Streamlit**: For creating an intuitive and interactive user interface.
- **PandasAI**: For integrating natural language queries with pandas dataframes.
- **LangChain**: For building conversational AI pipelines.
- **ChatGroq**: For offering a powerful large language model backend.
- **matplotlib**: For generating clear and informative visualizations.

Special thanks to the open-source community for their incredible contributions to these technologies!

---

## License

This project is licensed under the MIT License.
