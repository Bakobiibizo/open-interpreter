from src import (
    def_speaker, 
    elevenlabs_api, 
    get_api_keys, 
    get_audio_length, 
    JARVIS, 
    JARVIS_text_only, 
    open_interpreter_api, whisper_api
)

__all__ = [
    "def_speaker",
    "elevenlabs_api",
    "get_api_keys",
    "get_audio_length",
    "JARVIS",
    "JARVIS_text_only",
    "open_interpreter_api",
    "whisper_api"
]

from whisper_api import transcribe

transcribe("testing/test_file.wav")