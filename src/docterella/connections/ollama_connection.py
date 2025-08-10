import ollama

from docterella.connections.base_connection import BaseConnection
from typing import Dict

class OllamaConnection(BaseConnection):
    def __init__(self, model: str, options: Dict = None):
        self.model = model
        
        if options is None:
            self.options = {"temperature": 0, "top_p": 0.1}

    def prompt(self, prompt: str, format: str):
        result = ollama.generate(
            model=self.model, prompt=prompt, format=format, options=self.options
        )

        return result['response']