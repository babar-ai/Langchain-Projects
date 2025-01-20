# 🎙️ AI-Powered Voice Bot

## Overview

This project implements an AI-driven voice assistant capable of real-time speech-to-text transcription, natural language processing, and text-to-speech synthesis. By leveraging **Deepgram**, **LangChain**, and **ChatGroq**, the bot delivers a conversational experience, bridging human speech with advanced AI capabilities.

---

## Features

### 🗣️ Real-Time Speech-to-Text (STT)
- Converts live audio into text using **Deepgram**'s speech-to-text API.
- Processes user input seamlessly with minimal latency.

### 🤖 Natural Language Understanding
- Uses **ChatGroq** for generating conversational, context-aware responses.
- Integrates LangChain for memory-based interaction, ensuring context is retained across conversations.

### 🔊 Text-to-Speech (TTS)
- Converts AI-generated responses back into human-like speech using **Deepgram**'s TTS API.
- Delivers responses in a natural, conversational tone.

### 💬 Persistent Conversation
- Maintains conversation history with **ConversationBufferMemory**.
- Provides smooth, multi-turn dialogues by remembering context.

---

## Technologies Used

### Programming Languages
- **Python**

### Libraries and Tools
- **Deepgram**: For speech-to-text and text-to-speech processing.
- **LangChain**: Core framework for conversation and memory management.
- **ChatGroq**: Backend language model for generating natural language responses.
- **dotenv**: For managing environment variables.
- **asyncio**: For handling asynchronous operations.

---

## Prerequisites

1. **Install Python**:
   - Ensure Python 3.8 or higher is installed.

2. **Install Dependencies**:
   - Install required Python libraries using:
     ```bash
     pip install -r requirements.txt
     ```

3. **Set Up API Keys**:
   - Create a `.env` file in the project directory and include your API keys:
     ```plaintext
     DEEPGRAM_API_KEY=your_deepgram_api_key_here
     GROQ_API_KEY=your_groq_api_key_here
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

3. **Start the Bot**:
   ```bash
   python voice_bot.py
   ```

4. **Interact with the Bot**:
   - Speak into your microphone to initiate the conversation.
   - Say "goodbye" to end the interaction.

---

## Example Interaction

**User:** Hello, Eliza!  
**Eliza:** Hi there! How can I assist you today?  

**User:** Can you tell me about LangChain?  
**Eliza:** LangChain is a framework for building memory-aware conversational AI applications.  

**User:** goodbye  
**Eliza:** Goodbye! Have a great day!

---

## Folder Structure

```plaintext
📂 Project Directory
├── voice_bot.py           # Main application script
├── requirements.txt       # List of required dependencies
├── .env                   # API key configuration
├── README.md              # Project documentation
```

---

## Acknowledgments

Special thanks to:
- **Deepgram**: For advanced STT and TTS capabilities.
- **LangChain**: For enabling memory-based AI conversations.
- **ChatGroq**: For natural language understanding and generation.

---

## License

This project is licensed under the MIT License.
