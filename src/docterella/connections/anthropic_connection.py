import anthropic
import os

from docterella.connections.base_connection import BaseConnection
from typing import Dict

class AnthropicConnection(BaseConnection):
    def __init__(self, model, options: Dict = None):
        self.model = model
        
        if options is None:
            self.options = {"temperature": 0}

        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def prompt(self, instructions, prompt: str, format: str):

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=[
                {"type": "text", "text": instructions, "cache_control": {"type": "ephemeral"}},
                {"type": "text", "text": f"Your entire response must conform to this JSON schema\n{format}", "cache_control": {"type": "ephemeral"}},
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

        return "{" + message.content[0].text
