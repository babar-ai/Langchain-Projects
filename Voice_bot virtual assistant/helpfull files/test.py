import os
import requests
from dotenv import load_dotenv
import subprocess
import shutil
import time

# Load environment variables
load_dotenv()

# Set your Deepgram API Key
DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")

def is_installed(lib_name: str) -> bool:
    lib = shutil.which(lib_name)
    return lib is not None

def save_audio_to_file(audio_stream, save_path="output.pcm"):
    with open(save_path, "wb") as f:
        for chunk in audio_stream:
            if chunk:
                f.write(chunk)
    print(f"Audio saved to {save_path}")

def play_audio_file(file_path):
    if not is_installed("ffplay"):
        raise ValueError("ffplay is not installed. Install it to play audio.")
    
    player_command = ["ffplay", "-autoexit", "-nodisp", file_path]
    subprocess.run(player_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def send_tts_request(text):
    DEEPGRAM_URL = f"https://api.beta.deepgram.com/v1/speak"
    
    headers = {
        "Authorization": f"Token {DG_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text
    }
    
    # Make a POST request to Deepgram API
    with requests.post(DEEPGRAM_URL, stream=True, headers=headers, json=payload) as r:
        if r.status_code == 200:
            print("Request successful.")
            save_audio_to_file(r.iter_content(chunk_size=1024))
            play_audio_file("output.pcm")
        else:
            print(f"Error: {r.status_code}")
            print("Response content:", r.text)  # Print the error response for debugging

# Example usage
text = "my name is baber."
send_tts_request(text)
