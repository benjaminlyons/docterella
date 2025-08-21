import os
from openai import OpenAI
from pydantic import BaseModel
from typing import Dict
from docterella.connections.base_connection import BaseConnection

class OpenaiConnection(BaseConnection):
    def __init__(self, model, options: Dict = None):
        self.model = model

        if options is None:
            self.options = {"temperature": 0}

        self.client = OpenAI()

    def prompt(self, instructions, prompt: str, output_structure: BaseModel):
        message = self.client.responses.parse(
            model=self.model,
            instructions=instructions,
            input=prompt, 
            text_format=output_structure,
            **self.options,
        )

        return message.output_parsed.model_dump_json()
