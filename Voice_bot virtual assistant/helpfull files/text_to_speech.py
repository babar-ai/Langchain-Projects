# import os
# import requests
# import subprocess
# import shutil
# import time
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Set your Deepgram API Key and desired voice model
# DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# MODEL_NAME = "general"  # Use a supported model name, adjust as needed

# def is_installed(lib_name: str) -> bool:
#     return shutil.which(lib_name) is not None

# def save_audio_to_file(audio_stream, save_path="output.pcm"):
#     with open(save_path, "wb") as f:
#         for chunk in audio_stream:
#             if chunk:
#                 f.write(chunk)
#     print(f"Audio saved to {save_path}")

# def play_audio_file(file_path):
#     if not is_installed("ffplay"):
#         raise ValueError("ffplay is not installed. Install it to play audio.")
    
#     player_command = ["ffplay", "-autoexit", "-nodisp", file_path]
#     subprocess.run(player_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# def send_tts_request(text):
#     DEEPGRAM_URL = "https://api.beta.deepgram.com/v1/speak"
    
#     headers = {
#         "Authorization": f"Token {DG_API_KEY}",
#         "Content-Type": "application/json"
#     }
    
#     payload = {
#         "text": text
#     }
    
#     start_time = time.time()
    
#     try:
#         with requests.post(DEEPGRAM_URL, stream=True, headers=headers, json=payload) as r:
#             if r.status_code == 200:
#                 first_byte_time = None
#                 save_audio_to_file(r.iter_content(chunk_size=1024))
#                 play_audio_file("output.pcm")
#             else:
#                 print(f"Error: {r.status_code}")
#                 print("Response content:", r.text)
#     except requests.RequestException as e:
#         print(f"Request failed: {e}")

# # Example usage
# text = "The returns for performance are superlinear."
# send_tts_request(text)


import subprocess
import requests
import os
import shutil
class TextToSpeech:
    DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    MODEL_NAME = "aura-helios-en"  # Example model name, change as needed

    @staticmethod
    def is_installed(lib_name: str) -> bool:
        lib = shutil.which(lib_name)
        return lib is not None

    def speak(self, text):
        if not self.is_installed("ffplay"):
            raise ValueError("ffplay not found, necessary to stream audio.")

        DEEPGRAM_URL = f"https://api.deepgram.com/v1/speak?model={self.MODEL_NAME}&performance=true&encoding=linear16&sample_rate=24000"

        headers = {
            "Authorization": f"Token {self.DG_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "text": text
        }

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
                stderr=subprocess.PIPE,
            )

            for chunk in response.iter_content(chunk_size=1024):
                if chunk and player_process.stdin:
                    player_process.stdin.write(chunk)
                    player_process.stdin.flush()

            if player_process.stdin:
                player_process.stdin.close()
                player_process.wait()

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

# Test the TextToSpeech.speak() method
if __name__ == "__main__":
    tts = TextToSpeech()
    tts.speak("Hello, this is a test of the text-to-speech functionality.")
