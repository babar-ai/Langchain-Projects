
'''
what is transcribe?
"Transcribe" means to convert spoken language or audio into written text. This process involves listening to or processing
 audio (such as a conversation, speech, or lecture) and then accurately writing down what was said.
 
'''
import asyncio
import os
import requests
import shutil
import subprocess
import time
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.chains import LLMChain
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone
)

# Load environment variables from .env file
load_dotenv()
DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class LanguageModelProcessor:
    """Handles interactions with the language model."""
    
    def __init__(self):
        # Initialize language model and memory
        self.llm = ChatGroq(
            temperature=0,
            model_name="mixtral-8x7b-32768",
            groq_api_key=GROQ_API_KEY
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Define system prompt for the conversation model
        system_prompt = '''
        You are a conversational assistant named Eliza.
        Use short, conversational responses as if you're having a live conversation.
        Your response should be under 20 words.
        Do not respond with any code, only conversation
        '''
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{text}")
        ])

        # Create a conversation chain with the LLM
        self.conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory
        )

    def process(self, text):
        """Process user text and return the model's response."""
        self.memory.chat_memory.add_user_message(text)  # Add user message to memory

        start_time = time.time()
        response = self.conversation.invoke({"text": text})
        end_time = time.time()

        self.memory.chat_memory.add_ai_message(response['text'])  # Add AI response to memory

        elapsed_time = int((end_time - start_time) * 1000)
        print(f"LLM ({elapsed_time}ms): {response['text']}")
        return response['text']

class TextToSpeech:
    """Handles text-to-speech conversion using Deepgram."""
    
    MODEL_NAME = "aura-helios-en"  # Specify the desired voice model

    @staticmethod
    def is_installed(lib_name: str) -> bool:
        """Check if a library is installed."""
        return shutil.which(lib_name) is not None

    def speak(self, text):
        """Convert text to speech and play it back."""
        if not self.is_installed("ffplay"):
            raise ValueError("ffplay not found, necessary to stream audio.")

        DEEPGRAM_URL = f"https://api.deepgram.com/v1/speak?model={self.MODEL_NAME}&performance=true&encoding=linear16&sample_rate=24000"
        headers = {
            "Authorization": f"Token {DG_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"text": text}

        print(f"Sending request to Deepgram with text: {text}")

        try:
            response = requests.post(DEEPGRAM_URL, stream=True, headers=headers, json=payload)

            if response.status_code != 200:
                print(f"Deepgram API error: {response.status_code} - {response.text}")
                return

            player_command = ["ffplay", "-autoexit", "-", "-nodisp"]
            player_process = subprocess.Popen(
                player_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE
            )

            # Stream audio data to ffplay
            for chunk in response.iter_content(chunk_size=1024):
                if chunk and player_process.stdin:
                    player_process.stdin.write(chunk)
                    player_process.stdin.flush()

            if player_process.stdin:
                player_process.stdin.close()
                player_process.wait()

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

class TranscriptCollector:
    """Collects and manages parts of the transcript."""
    
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset the transcript collector."""
        self.transcript_parts = []

    def add_part(self, part):
        """Add a part to the transcript."""
        self.transcript_parts.append(part)

    def get_full_transcript(self):
        """Get the full transcript as a single string."""
        return ' '.join(self.transcript_parts)

transcript_collector = TranscriptCollector()
async def get_transcript(callback):
    """Stream audio from the microphone and transcribe it using Deepgram."""
    transcription_complete = asyncio.Event()  # Event to signal transcription completion

    try:
        config = DeepgramClientOptions(options={"keepalive": "true"})
        deepgram = DeepgramClient(DG_API_KEY, config)
        dg_connection = deepgram.listen.asyncwebsocket.v("1")
        print("Listening...")

        async def on_message(result, *args, **kwargs):
            """Handle transcription messages."""
            sentence = result.channel.alternatives[0].transcript

            if not result.speech_final:
                transcript_collector.add_part(sentence)
            else:
                transcript_collector.add_part(sentence)
                full_sentence = transcript_collector.get_full_transcript()
                if full_sentence.strip():
                    print(f"Human: {full_sentence.strip()}")
                    callback(full_sentence.strip())  # Call the callback with the full_sentence
                    transcript_collector.reset()
                    transcription_complete.set()  # Signal to stop transcription and exit

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model="nova-2",
            punctuate=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            endpointing=300,
            smart_format=True
        )

        await dg_connection.start(options)

        # Open a microphone stream on the default input device
        microphone = Microphone(dg_connection.send)
        microphone.start()

        await transcription_complete.wait()  # Wait for the transcription to complete

        microphone.finish()
        await dg_connection.finish()

    except Exception as e:
        print(f"Could not open socket: {e}")


class ConversationManager:
    """Manages the conversation flow between transcription, language model, and text-to-speech."""

    def __init__(self):
        self.transcription_response = ""
        self.llm = LanguageModelProcessor()

    async def main(self):
        """Main loop for handling conversation."""
        def handle_full_sentence(full_sentence):
            """Handle completed transcription."""
            self.transcription_response = full_sentence
            print(f"Received transcription: {full_sentence}")

        print("Starting conversation loop...")
        while True:
            try:
                await get_transcript(handle_full_sentence)

                if "goodbye" in self.transcription_response.lower():
                    print("Ending conversation.")
                    break

                print(f"Processing LLM response for: {self.transcription_response}")
                llm_response = self.llm.process(self.transcription_response)
                print(f"LLM response: {llm_response}")

                print("Generating voice response...")
                tts = TextToSpeech()
                tts.speak(llm_response)

                self.transcription_response = ""

            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    manager = ConversationManager()
    asyncio.run(manager.main())
