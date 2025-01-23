from abc import ABC, abstractmethod
from typing import Type

class BaseController(ABC):

    @abstractmethod
    def retrieve_response(self, user_input: str) -> str:
        """Process the input and return the response from the LLM"""
        pass

   
   
    