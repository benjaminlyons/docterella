from pydantic import BaseModel

from typing import List

class DocstringArgument(BaseModel):
    # name of the argument
    name: str

    # string representation of the argument type (e.g., bool)
    data_type: str

    # description of the argument
    description: str

class DocstringReturnValue(BaseModel):
    data_type: str
    description: str

class CorrectedDocstring(BaseModel):
    # one line description of the function 
    correct_function_description: str

    # list of expected docstring arguments
    correct_function_arguments: List[DocstringArgument]

    correct_function_return_values: List[DocstringReturnValue]

class DocstringValidation(BaseModel):
    function_name: str

    docstring_argument_names_match_function_signature: bool
    docstring_argument_types_are_correct: bool
    docstring_arguments_are_accepted: bool
    docstring_argument_descriptions_are_correct: bool
    has_accurate_return_type: bool

    # proposed docstring
    corrected_function_docstring: CorrectedDocstring

    summary_of_findings: str
