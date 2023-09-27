import os
import json
import loguru
import appdirs

from datetime import datetime, tzinfo
from dotenv import load_dotenv
from typing import Union, Callable, Any, List, Dict
from pathlib import Path
from interpreter.core.core_models import InterpreterABC, InterpreterModel
from interpreter.core.respond import respond
from interpreter.cli.cli import cli
from interpreter.utils.check_for_update import check_for_update
from interpreter.utils.display_markdown_message import display_markdown_message
from interpreter.llm.setup_llm import setup_llm
from interpreter.terminal_interface.terminal_interface import terminal_interface
from interpreter.terminal_interface.validate_llm_settings import validate_llm_settings

path = Path
load_dotenv()

logger = loguru.logger

    
def default_interpreter_config(    
        messages: Union[List[Dict[str, str]], None]=[],
        _code_interpreter: Union[Dict[str, str], None]={},
        local: bool=False,
        auto_run: bool=False,
        debug_mode: bool=False,
        max_output: int=2000,
        conversation_history: bool=True,
        conversation_name: Callable[[tzinfo | None], datetime]=datetime.now().strftime("%B_%d_%Y_%H-%M-%S"),
        conversation_history_path: str = str(path.cwd() / appdirs.user_data_dir("Open Interpreter") / "conversations"),
        model: str= "gpt-3.5-turbo",
        temperature: float=1.5,
        system_message: str="",
        context_window: Union[str, None]=None,
        max_tokens: Union[int, None]=None,
        api_base: Union[str, None]=None,
        api_key: Union[str, None]=os.environ["OPENAI_API_KEY"],
        max_budget: Union[int, None]=None,
        _llm: Union[str, None]=None,
    ) -> Dict[str, Any]: 
    """
    Generates the default configuration for the interpreter.

    :param messages: A list of dictionaries representing the chat messages. Defaults to an empty list.
    :param _code_interpreter: A dictionary representing the code interpreter. Defaults to an empty dictionary.
    :param local: A boolean indicating whether the interpreter is running locally. Defaults to False.
    :param auto_run: A boolean indicating whether the interpreter should automatically run the code. Defaults to False.
    :param debug_mode: A boolean indicating whether the interpreter is in debug mode. Defaults to False.
    :param max_output: An integer representing the maximum length of the output. Defaults to 2000.
    :param conversation_history: A boolean indicating whether the conversation history should be stored. Defaults to True.
    :param conversation_name: A callable function that returns the name of the conversation. Defaults to the current datetime.
    :param conversation_history_path: A string representing the path to store the conversation history. Defaults to the 'conversations' directory in the user's data directory.
    :param model: A string representing the model to use for the interpreter. Defaults to 'gpt-3.5-turbo'.
    :param temperature: A float representing the temperature of the model. Defaults to 1.5.
    :param system_message: A string representing the system message. Defaults to an empty string.
    :param context_window: A string or None representing the context window. Defaults to None.
    :param max_tokens: An integer or None representing the maximum number of tokens. Defaults to None.
    :param api_base: A string or None representing the API base URL. Defaults to None.
    :param api_key: A string or the value of the 'OPENAI_API_KEY' environment variable representing the API key. Defaults to the value of the 'OPENAI_API_KEY' environment variable.
    :param max_budget: An integer or None representing the maximum budget. Defaults to None.
    :param _llm: A string or None representing the LLM. Defaults to None.
    :return: A dictionary representing the default interpreter configuration.
    """
    logger.info("> default_interpreter_config")
    return {
        "messages":messages,
        "_code_interpreters":_code_interpreter,
        "local":local,
        "auto_run":auto_run,
        "debug_mode":debug_mode,
        "max_output":max_output,
        "conversation_history":conversation_history,
        "conversation_name":conversation_name,
        "conversation_history_path":conversation_history_path,
        "model":model,
        "temperature":temperature,
        "system_message":system_message,
        "context_window":context_window,
        "max_tokens":max_tokens,
        "api_base":api_base,
        "api_key":api_key,
        "max_budget":max_budget,
        "_llm":_llm,
    }

class OpenInterpreter(InterpreterABC):
    def __init__(self, data: InterpreterModel=default_interpreter_config()) -> None:
        logger.info("> OpenInterpreter.__init__")
        super().__init__()
        self.messages = data["messages"]
        self._code_interpreters = data["_code_interpreters"]
        self.local = data["local"]
        self.auto_run = data["auto_run"]
        self.debug_mode = data["debug_mode"]
        self.max_output = data["max_output"]
        self.conversation_history = data["conversation_history"]
        self.conversation_name = data["conversation_name"]
        self.conversation_history_path = data["conversation_history_path"]
        self.model = data["model"]
        self.temperature = data["temperature"]
        self.system_message = data["system_message"]
        self.context_window = data["context_window"]
        self.max_tokens = data["max_tokens"]
        self.api_base = data["api_base"]
        self.api_key = data["api_key"]
        self.max_budget = data["max_budget"]
        self._llm = data["_llm"]
        # Check for update
        if not self.local:
            # This should actually be pushed into the utility
            if check_for_update():
                display_markdown_message("> **A new version of Open Interpreter is available.**\n>Please run: `pip install --upgrade open-interpreter`\n\n---")
        
    def cli(self)-> None:
        logger.info("> OpenInterpreter.cli")
        cli(self)
        
    def chat(self, message: Union[str, None]=None, display: bool=True, stream: bool=False) -> Any:
        if stream:
            return self._streaming_chat(message=message, display=display)
        
        # If stream=False, *pull* from the stream.
        for _ in self._streaming_chat(message=message, display=display):
            pass
        
        return self.messages
        
    def _streaming_chat(self, message: Union[str, None]=None, display: bool=True)-> Any:
        logger.info("> OpenInterpreter._streaming_chat")

        # If we have a display,
        # we can validate our LLM settings w/ the user first
        if display:
            validate_llm_settings(self)

        # Setup the LLM
        if not self._llm:
            self._llm = setup_llm(self)

        # Sometimes a little more code -> a much better experience!
        # Display mode actually runs interpreter.chat(display=False, stream=True) from within the terminal_interface.
        # wraps the vanilla .chat(display=False) generator in a display.
        # Quite different from the plain generator stuff. So redirect to that
        if display:
            yield from terminal_interface(self, message)
            return
        
        # One-off message
        if message:
            self.messages.append({"role": "user", "message": message})
            
            yield from self._respond()

            # Save conversation
            if self.conversation_history:
                # Check if the directory exists, if not, create it
                if not os.path.exists(self.conversation_history_path):
                    os.makedirs(self.conversation_history_path)
                # Write or overwrite the file
                with open(os.path.join(self.conversation_history_path, self.conversation_name + '.json'), 'w', encoding='utf-8') as f:
                    json.dump(self.messages, f)
                
            return
        
        raise RuntimeError("`interpreter.chat()` requires a display. Set `display=True` or pass a message into `interpreter.chat(message)`.")
        
    def _respond(self) -> Any:
        logger.info("> OpenInterpreter._respond")
        yield from respond(self)
            
    def reset(self)-> None:
        logger.info("> OpenInterpreter.reset")
        self.messages = []
        self.conversation_name = datetime.now().strftime("%B %d, %Y")
        for code_interpreter in self._code_interpreters.values():
            code_interpreter.terminate()
        self._code_interpreters = {}
        
interpreter = OpenInterpreter()

def get_interpreter() -> OpenInterpreter:
    logger.info("> get_interpreter")
    return interpreter


if __name__ == "__main__":
    get_interpreter()