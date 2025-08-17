import ast
import astor

from docterella.components.assessment import FunctionDocstringAssessment
from docterella.components.assessment import ClassDocstringAssessment
from docterella.connections.base_connection import BaseConnection
from docterella.prompts.function_prompt import FUNCTION_PROMPT
from docterella.prompts.class_prompt import CLASS_PROMPT
from docterella.components.results import ValidationResults
from docterella.parsers.function_parser import FunctionMetadata
from docterella.parsers.class_parser import ClassMetadata

class ValidationAgent:
    def __init__(self, connection: BaseConnection):
        self.connection = connection
        self.function_instructions = FUNCTION_PROMPT # COT_FUNCTION_PROMPT
        self.class_instructions = CLASS_PROMPT

    def validate_function(self, function: FunctionMetadata):
        """Validate docstrings for the provided function

        Parameters
        ----------
        function_node: ast.FunctionDef
            The ast.FunctionDef representation of the Python function to examine

        Returns
        -------
        str
            Return a JSON representation of the validation results, must be compliant
            with the `DocstringValidation` schema.
        """
        response = self.connection.prompt(
            instructions=self.function_instructions,
            prompt=function.source,
            format=FunctionDocstringAssessment.model_json_schema()
        )

        try:
            da = FunctionDocstringAssessment.model_validate_json(response)
        except Exception as e:
            print(response)
            raise e

        return ValidationResults(function, da)
    
    def validate_class(self, cls: ClassMetadata):
        source = cls.constructor.source
        docstring = cls.docstring

        prompt = (
            f"<docstring>{docstring}</docstring>\n"
            f"<constructor>{source}</constructor>\n"
        )

        response = self.connection.prompt(
            instructions=self.class_instructions,
            prompt=prompt,
            format=ClassDocstringAssessment.model_json_schema(),
        )

        try:
            cda = ClassDocstringAssessment.model_validate_json(response)
        except Exception as e:
            print(response)
            raise e
        
        return ValidationResults(cls, cda)
