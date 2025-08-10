from pydantic import BaseModel

from typing import List

class Argument(BaseModel):
    # name of the argument
    name: str

    # string representation of the argument type (e.g., bool)
    data_type: str

    # description of the argument
    description: str

class ReturnValue(BaseModel):
    data_type: str
    description: str

class FunctionDocstring(BaseModel):
    # one line description of the function 
    correct_function_description: str

    # list of expected docstring arguments
    correct_function_arguments: List[Argument]

    correct_function_return_values: List[ReturnValue]

class FunctionDocstringAssessment(BaseModel):
    function_name: str

    docstring_argument_names_match_signature: bool
    docstring_argument_types_are_correct: bool
    docstring_arguments_are_accepted: bool
    docstring_argument_descriptions_are_correct: bool
    has_accurate_return_type: bool

    corrected_function_docstring: FunctionDocstring

    summary_of_findings: str

class ClassDocstring(BaseModel):
    correct_class_description: str
    correct_class_arguments: List[Argument]

class ClassDocstringAssessment(BaseModel):
    class_name: str

    docstring_argument_names_match_constructor: bool
    docstring_argument_types_are_correct: bool
    docstring_arguments_are_accepted: bool
    docstring_argument_descriptions_are_correct: bool

    corrected_class_docstring: ClassDocstring

    summary_of_findings: str

