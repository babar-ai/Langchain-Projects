import asyncio
import os
import time
import requests
import shutil
import subprocess
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

# Load environment variables
load_dotenv()
DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")


# Language Model Processor
class LanguageModelProcessor:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0, model_name="mixtral-8x7b-32768", groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        system_prompt = """
        You are a conversational assistant named Eliza.
        Use short, conversational responses as if you're having a live conversation.
        Your response should be under 20 words.
        Do not respond with any code, only conversation.
        """

        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{text}")
        ])

        self.conversation = LLMChain(llm=self.llm, prompt=self.prompt, memory=self.memory)

    def process(self, text):
        self.memory.chat_memory.add_user_message(text)  # Add user message to memory

        start_time = time.time()
        response = self.conversation.invoke({"text": text})  # Get LLM response
        elapsed_time = int((time.time() - start_time) * 1000)

        self.memory.chat_memory.add_ai_message(response['text'])  # Add AI response to memory
        print(f"LLM ({elapsed_time}ms): {response['text']}")
        return response['text']


# Text-to-Speech
class TextToSpeech:
    MODEL_NAME = "aura-helios-en"

    def __init__(self):
        self.DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")

    @staticmethod
    def is_installed(lib_name: str) -> bool:
        return shutil.which(lib_name) is not None

    def speak(self, text):
        if not self.is_installed("ffplay"):
            raise ValueError("ffplay not found, necessary to stream audio.")

        DEEPGRAM_URL = f"https://api.deepgram.com/v1/speak?model={self.MODEL_NAME}&performance=true&encoding=linear16&sample_rate=24000"
        headers = {
            "Authorization": f"Token {self.DG_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"text": text}

        try:
            response = requests.post(DEEPGRAM_URL, stream=True, headers=headers, json=payload)
            if response.status_code != 200:
                print(f"Deepgram API error: {response.status_code} - {response.text}")
                return

            audio_data = response.content
            player_command = ["ffplay", "-autoexit", "-", "-nodisp"]
            player_process = subprocess.Popen(player_command, stdin=subprocess.PIPE)

            if player_process.stdin:
                player_process.stdin.write(audio_data)
                player_process.stdin.close()
            player_process.wait()

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")


# Transcript Collector
class TranscriptCollector:
    def __init__(self):
        self.reset()

    def reset(self):
        self.transcript_parts = []

    def add_part(self, part):
        self.transcript_parts.append(part)

    def get_full_transcript(self):
        return ' '.join(self.transcript_parts)


# Get Transcript (Speech-to-Text)
async def get_transcript(callback):
    transcription_complete = asyncio.Event()
    transcript_collector = TranscriptCollector()

    try:
        deepgram_client = DeepgramClient()
        dg_connection = deepgram_client.listen.asyncwebsocket.v("1")

        async def on_message(_, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if not result.speech_final:
                transcript_collector.add_part(sentence)
            else:
                transcript_collector.add_part(sentence)
                full_sentence = transcript_collector.get_full_transcript().strip()
                if full_sentence:
                    print(f"Human: {full_sentence}")
                    callback(full_sentence)
                    transcript_collector.reset()
                    transcription_complete.set()

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        options = LiveOptions(model="nova-2", punctuate=True, language="en-US", encoding="linear16")
        await dg_connection.start(options)

        microphone = Microphone(dg_connection.send)
        microphone.start()
        await transcription_complete.wait()
        microphone.finish()
        await dg_connection.finish()

    except Exception as e:
        print(f"Could not open socket: {e}")


# Conversation Manager
class ConversationManager:
    def __init__(self):
        self.transcription_response = ""
        self.llm = LanguageModelProcessor()

    async def main(self):
        def handle_full_sentence(full_sentence):
            self.transcription_response = full_sentence

        while True:
            try:
                await get_transcript(handle_full_sentence)
                if "goodbye" in self.transcription_response.lower():
                    print("Ending conversation.")
                    break

                llm_response = self.llm.process(self.transcription_response)
                tts = TextToSpeech()
                tts.speak(llm_response)
                self.transcription_response = ""

            except Exception as e:
                print(f"An error occurred: {e}")


# Run the Voice Bot
if __name__ == "__main__":
    manager = ConversationManager()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(manager.main())
