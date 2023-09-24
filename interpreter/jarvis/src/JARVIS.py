import gradio as gr
import whisper
import interpreter

from speak import speak
from whisper_api import model

last_sentence = ""

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    audio_input = gr.inputs.Audio(source="microphone", type="filepath")
    btn = gr.Button("Submit")
    clear = gr.Button("Clear")

    def transcribe(audio):
      audio = whisper.load_audio(audio)
      audio = whisper.pad_or_trim(audio)
      mel = whisper.log_mel_spectrogram(audio).to(model.device)
      _, probs = model.detect_language(mel)
      options = whisper.DecodingOptions()
      result = whisper.decode(model, mel, options)
      return result.text

    def add_user_message(audio, history):
        user_message = transcribe(audio)
        return history + [[user_message, None]]

    def bot(history):
        global last_sentence

        user_message = history[-1][0]
        history[-1][1] = ""
        active_block_type = ""
        language = ""
        for chunk in interpreter.chat(user_message, stream=True, display=False):

            # Message
            if "message" in chunk:
              if active_block_type != "message":
                active_block_type = "message"
              history[-1][1] += chunk["message"]

              last_sentence += chunk["message"]
              if any([punct in last_sentence for punct in ".?!\n"]):
                speak(last_sentence)
                last_sentence = ""

              yield history

            # Code
            if "language" in chunk:
              language = chunk["language"]
            if "code" in chunk:
              if active_block_type != "code":
                active_block_type = "code"
                history[-1][1] += f"\n```{language}"
              history[-1][1] += chunk["code"]
              yield history

            # Output
            if "executing" in chunk:
              history[-1][1] += "\n```\n\n```text\n"
              yield history
            if "output" in chunk:
              if chunk["output"] != "KeyboardInterrupt":
                history[-1][1] += chunk["output"] + "\n"
                yield history
            if "active_line" in chunk and chunk["active_line"] == None:
              history[-1][1] = history[-1][1].strip()
              history[-1][1] += "\n```\n"
              yield history

    btn.click(add_user_message, [audio_input, chatbot], [chatbot]).then(
        bot, chatbot, chatbot
    )

    clear.click(lambda: None, None, chatbot, queue=False)

demo.queue()
demo.launch(debug=True)