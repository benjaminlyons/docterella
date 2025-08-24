from abc import ABC, abstractmethod
from pydantic import BaseModel

class BaseConnection(ABC):
    """Interface for connections to an LLM api (e.g., Ollama)"""
    @abstractmethod
    def prompt(
        self, instructions: str, prompt: str, output_structure: BaseModel
    ) -> str:
        """Sends a request to the model and returns the response
        
        Parameters
        ----------
        instructions: str
            The system prompt style instructions that provide the model a role
            and business rules for evaluations. This should not include the
            function/class that will be evaluated

        prompt: str
            The code and docstrings for evaluation

        output_structure: BaseModel
            A Pydantic class that specifies the expected format and typing for
            the response
        """
        pass
