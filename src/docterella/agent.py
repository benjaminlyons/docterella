import ast
import astor

from docterella.components.assessment import DocstringAssessment
from docterella.connections.base_connection import BaseConnection
from docterella.prompts.function_prompt import FUNCTION_PROMPT
from docterella.components.results import ValidationResults
from docterella.parsers.function_parser import FunctionMetadata

class ValidationAgent:
    def __init__(self, connection: BaseConnection):
        self.connection = connection
        self.function_instructions = FUNCTION_PROMPT

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
        source = function.source

        prompt = f"{self.function_instructions}\n<code>{source}</code>\n"

        response = self.connection.prompt(
            prompt, format=DocstringAssessment.model_json_schema()
        )

        da = DocstringAssessment.model_validate_json(response)

        return ValidationResults(function, da)