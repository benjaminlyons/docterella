import anthropic
import os

from pydantic import BaseModel
from docterella.connections.base_connection import BaseConnection
from typing import Dict

class AnthropicConnection(BaseConnection):
    """Interface for connecting with Anthropics models"""
    def __init__(self, model, options: Dict = None):
        self.model = model
        
        if options is None:
            self.options = {"temperature": 0}

        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def prompt(self, instructions: str, prompt: str, output_structure: BaseModel):
        format = output_structure.model_json_schema()

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=[
                {
                    "type": "text", 
                    "text": instructions, 
                    "cache_control": {"type": "ephemeral"}
                },
                {
                    "type": "text", 
                    "text": f"Your entire response MUST be ONLY perfect, VALID, PARSEABLE JSON that conforms to this JSON schema\n{format}", 
                    "cache_control": {"type": "ephemeral"}
                },
            ],
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
                {
                    "role": "assistant",
                    "content": "{",
                }
            ]
        )

        result = "{" + message.content[0].text
        
        return result
