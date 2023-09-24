"""
This file defines the abstract base class and base model classes for the interpreter class. the abstract base class is used to define the types of functions that the interpreter class will have and the model defines how that model will interact with data. 
It's the main file. `import interpreter` will import an instance of this class.
"""
from interpreter.utils import display_markdown_message
from ..cli.cli import cli
from ..utils.get_config import get_config
from .respond import respond
from ..llm.setup_llm import setup_llm
from ..terminal_interface.terminal_interface import terminal_interface
from ..terminal_interface.validate_llm_settings import validate_llm_settings
import appdirs
import os
import json
from datetime import datetime
from ..utils.check_for_update import check_for_update
from ..utils.display_markdown_message import display_markdown_message
from pydantic import BaseModel
from ABC import ABC
from ABC import abstractmethod


class InterpreterModel(BaseModel):
    
       # State
    messages: List
    _code_interpreters: Dict

    # Settings
    local: bool
    auto_run: bool
    debug_mode: bool
    max_output: int

    # Conversation history
    conversation_history: bool
    conversation_name: str
    conversation_history_path: str

    # LLM settings
    model: str
    temperature: int
    system_message: str
    context_window: Union[str, None]
    max_tokens: Union[int, None]
    api_base: Union[str, None]
    api_key: Union[str, None]
    max_budget: Union[int, None]
    _llm: Union[str, None]
    
    def __init__(self, **data):
        super().__init__(**data)
    
    # Load config defaults
    config = self.get_configuration_file()
    
    #turns the config file contents into a dictionary for easy access
    # should consider another method for setting these values rather than directly updating __dict__
    __dict__.update(config)

    def get_configuration_file(self) -> str:
        """This method should be implemented in the concrete class and should return the config as a string."""
        raise NotImplementedError("You must implement this method in the concrete class.")

class InterpreterABC(ABC):
    @abstractmethod
    def cli(cls, **data: InterpterterModel(**data))-> None:
        cli(cls, , **data: InterpterterModel(**data))
        
    @abstractmethod
    def __init__(cls)-> None:
        "Along with setting the configuration it should also check for updates and that check should be pushed into the utility."

    @abstractmethod
    def chat(cls, message=None, display=bool, stream=bool)-> List[Dict[str, str]] :
        "should handle all the chat functionality. consider breaking this into smaller function each responsible for inidivdual tasks."
        pass

    @abstractmethod
     def _streaming_chat(self, message=None, display=True)-> None:
         """
         Yields tokens, but also adds them to interpreter.messages. TBH probably would be good to seperate those two responsibilities someday soon
         Responds until it decides not to run any more code or say anything else.
         """
         pass
     
    def _respond(self) -> None:
        yield from respond(self)
        
    @abstractmethod
    def reset(self) -> None:
        """Reset the state."""
        pass
