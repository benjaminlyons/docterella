import ollama

from pydantic import BaseModel
from docterella.connections.base_connection import BaseConnection
from typing import Dict

class OllamaConnection(BaseConnection):
    """Interface for connecting to a model running via Ollama"""
    def __init__(self, model: str, options: Dict = None):
        self.model = model
        
        if options is None:
            self.options = {"temperature": 0}

    def prompt(
        self, 
        instructions: str,
        prompt: str, 
        output_structure: BaseModel,
    ):

        result = ollama.generate(
            model=self.model, 
            prompt=f"{instructions}<code>{prompt}</code>", 
            format=output_structure.model_json_schema(), 
            options=self.options
        )

        return result['response']
