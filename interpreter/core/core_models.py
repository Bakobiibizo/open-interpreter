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
    """
    Pydantic data model to determine the configuration of the Interpreter

    Args:
        BaseModel: Pydantic data model
    
    Returns:
        InterpreterModel
        
    Attributes:
        messages: List
        _code_interpreters: Dict
        local: bool
        auto_run: bool
        debug_mode: bool
        max_output: int
        conversation_history: bool
        conversation_name: str
        conversation_history_path: str
        model: str
        temperature: int
        system_message: str
        context_window: Union[str, None]
        max_tokens: Union[int, None]
        api_base: Union[str, None]
        api_key: Union[str, None]
        max_budget: Union[int, None]
        _llm: Union[str, None]
        
    Methods:
        __init__(self, **data):
    """
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
        """
        Initializes a new instance of the class.

        Args:
            **data: The keyword arguments that will be passed to the parent class.

        Returns:
            None
        """
        super().__init__(**data)

class InterpreterABC(ABC):
    @abstractmethod
    def __init__(self)-> None:
        """
        Abstract Base Class for the Interpreter Class
        
        Returns:
            None

        Yields:
            None
        """
        
    @abstractmethod
    def cli(self)-> None:
        """
        A function that represents the command line interface (CLI) for this class.

        :returns: None
        """
        cli(self)
    @abstractmethod
    def chat(self, message=None, display=bool, stream=bool)-> List[Dict[str, str]] :
        """
        should handle all the chat functionality. consider breaking this into smaller function each responsible for inidivdual tasks.
        """
        
        pass

    @abstractmethod
    def _streaming_chat(self, message=None, display=True)-> None:
         """
         Yields tokens, but also adds them to interpreter.messages. TBH probably would be good to seperate those two responsibilities someday soon
         Responds until it decides not to run any more code or say anything else.
         """
         pass
     
    def _respond(self) -> None:
        """
        This function is a private method named _respond.
        It does not take any parameters.
        It does not return anything.
        """
        yield from respond(self)
        
    @abstractmethod
    def reset(self) -> None:
        """
        Reset the state.
        """
        pass
