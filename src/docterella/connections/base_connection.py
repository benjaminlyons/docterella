from abc import ABC, abstractmethod

class BaseConnection(ABC):

    @abstractmethod
    def prompt(self, prompt: str, format: str) -> str:
        pass