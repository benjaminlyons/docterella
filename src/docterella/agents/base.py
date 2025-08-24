from abc import ABC
from abc import abstractmethod

from docterella.connections.base_connection import BaseConnection

from docterella.results import ValidationResults
from docterella.pydantic.metadata import FunctionMetadata
from docterella.pydantic.metadata import ClassMetadata

from docterella.agents.config import AgentConfig
from docterella.agents.config import BasicConfig

class ValidationAgent:
    def __init__(
        self, 
        connection: BaseConnection, 
        config: AgentConfig = None,
    ):
        if config is None:
            config = BasicConfig()

        self.connection = connection
        self.config = config

    def validate_function(self, function: FunctionMetadata):
        response = self.connection.prompt(
            instructions=self.function_prompt,
            prompt=function.source_code,
            output_structure=self.function_output
        )

        try:
            da = self.function_output.model_validate_json(response)
        except Exception as e:
            print(response)
            raise e

        return ValidationResults(function, da)

    def validate_class(self, cls: ClassMetadata):
        source = cls.constructor.source_code
        docstring = cls.docstring

        prompt = (
            f"<docstring>{docstring}</docstring>\n"
            f"<constructor>{source}</constructor>\n"
        )

        response = self.connection.prompt(
            instructions=self.class_prompt,
            prompt=prompt,
            output_structure=self.class_output,
        )

        try:
            cda = self.class_output.model_validate_json(response)
        except Exception as e:
            print(response)
            raise e
        
        return ValidationResults(cls, cda)
    
    @property
    def function_prompt(self):
        return self.config.function_prompt
    
    @property
    def class_prompt(self):
        return self.config.class_prompt
    
    @property
    def function_output(self):
        return self.config.function_output
    
    @property
    def class_output(self):
        return self.config.class_output
