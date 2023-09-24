import gradio as gr
import interpreter

from get_api_keys import get_api_keys

openai_api_key = get_api_keys()[1]

interpreter.api_key = openai_api_key
interpreter.auto_run = True

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
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
              yield history

            # Code
            if "language" in chunk:
              language = chunk["language"]
            if "code" in chunk:
              if active_block_type != "code":
                active_block_type = "code"
                history[-1][1] += f"\n```{language}\n"
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

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)


demo.queue()
demo.launch(debug=True)