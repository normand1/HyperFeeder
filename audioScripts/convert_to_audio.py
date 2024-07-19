import os
import sys
import requests
from dotenv import load_dotenv


currentFile = os.path.realpath(__file__)
currentDirectory = os.path.dirname(currentFile)
load_dotenv(os.path.join(currentDirectory, ".env.audioScripts"))
load_dotenv(os.path.join(currentDirectory, "../.env"))

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1024"))  # Default to 1024 if not set
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{os.getenv('VOICE_ID')}"


def convert_text_to_audio(text_file, audio_file):
    with open(text_file, "r") as file:
        text = file.read()

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.getenv("XI_API_KEY"),
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    response = requests.post(API_URL, json=data, headers=headers)
    response.raise_for_status()

    with open(audio_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_to_audio.py <text_file> <audio_file>")
        sys.exit(1)

    text_file = sys.argv[1]
    audio_file = sys.argv[2]

    try:
        convert_text_to_audio(text_file, audio_file)
        print(f"Successfully converted {text_file} to {audio_file}")
    except Exception as e:
        print(f"Failed to convert {text_file} to {audio_file}: {e}")
        sys.exit(1)
