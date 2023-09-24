import os
import getpass
from dotenv import load_dotenv

load_dotenv()


def get_api_keys():
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not elevenlabs_api_key:
        elevenlabs_api_key = getpass.getpass(prompt='Eleven Labs API Key: ', stream=None)
    
    if not openai_api_key:
        openai_api_key = getpass.getpass(prompt='OpenAI API Key: ', stream=None)
    
    return elevenlabs_api_key, openai_api_key

