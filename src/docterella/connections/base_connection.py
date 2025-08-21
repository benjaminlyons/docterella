from abc import ABC, abstractmethod
from pydantic import BaseModel

class BaseConnection(ABC):

    @abstractmethod
    def prompt(self, instructions: str, prompt: str, output_structure: BaseModel) -> str:
        pass
