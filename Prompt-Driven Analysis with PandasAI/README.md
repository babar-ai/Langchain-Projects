# 📊 Prompt-Driven Analysis with PandasAI

## Overview

This project enables users to interactively analyze data in CSV files using natural language queries. It leverages **PandasAI**, a smart dataframe library, in combination with the **ChatGroq LLM**, to provide prompt-driven insights directly from uploaded data. The interface is built using **Streamlit** for a user-friendly experience.

---

## Key Features

### 🔗 Seamless File Upload
- Upload CSV files to begin analysis.
- Automatically reads and displays a preview of the uploaded data.

### 🧠 AI-Powered Data Analysis
- Uses **PandasAI** to process user queries and perform advanced data operations without writing any code.
- Supports natural language prompts to extract meaningful insights from your data.

### 🎨 Visualization Support
- The project integrates **matplotlib**, making it easy to generate and display visualizations for data-driven questions.

### 🛠️ Streamlit Interface
- A clean and intuitive interface allows users to interact with the tool effortlessly.
- Prompts and results are displayed alongside a logo for branding.

---

## Technologies Used

### Programming Languages
- **Python**: Core language for development.

### Libraries and Frameworks
- **Streamlit**: Provides the interactive user interface.
- **Pandas**: Handles data processing and manipulation.
- **PandasAI**: Extends pandas with LLM-driven query support.
- **matplotlib**: Used for generating visualizations.
- **LangChain Groq**: Integrates ChatGroq as the LLM backend.

### Environment Management
- **dotenv**: Loads API keys and environment variables.

---

## Prerequisites

### Environment Setup
- Python 3.8 or higher is recommended.
- Install the required dependencies:
```bash
pip install -r requirements.txt

## How It Works

1. **File Upload**: Upload a CSV file via the Streamlit interface.
2. **Data Preview**: The app displays the first few rows of the file for a quick overview.
3. **Prompt Input**: Enter a natural language question about the data.
4. **AI Response**: The LLM processes the query and provides a detailed response or visualization.

## Running the Application

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>

## Example Use Case

1. **Upload a Dataset**:
   Upload a CSV file containing your data, such as `sales.csv`.

2. **Ask Questions**:
   Use natural language to query the data, for example:
   - "What are the top 5 products by revenue?"
   - "Show me a line graph of monthly sales trends."

3. **Receive Insights**:
   The app processes your queries and provides:
   - Textual responses with insights.
   - Visualizations (e.g., line graphs or bar charts) based on your data.
