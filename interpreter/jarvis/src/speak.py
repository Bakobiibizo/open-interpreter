import time
from elevenlabs import generate, play

from get_audio_length import get_audio_length
def speak(text):
  speaking = True
  audio = generate(
      text=text,
      voice="Master Cheif"
  )
  play(audio, notebook=True)

  audio_length = get_audio_length(audio)
  time.sleep(audio_length)
  