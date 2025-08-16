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
    summary_of_findings: str

    parameter_names_are_correct: bool
    parameter_types_are_correct: bool
    parameter_descriptions_are_correct: bool
    return_type_is_correct: bool

    corrected_function_docstring: FunctionDocstring

    @property
    def docstring(self):
        return self.corrected_function_docstring


class ClassDocstring(BaseModel):
    correct_class_description: str
    correct_class_arguments: List[Argument]

class ClassDocstringAssessment(BaseModel):
    parameter_names_are_correct: bool
    parameter_types_are_correct: bool
    parameter_descriptions_are_correct: bool

    corrected_class_docstring: ClassDocstring

    summary_of_findings: str

    @property
    def docstring(self):
        return self.corrected_class_docstring

