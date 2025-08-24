from pydantic import BaseModel

from docterella.pydantic.components import Argument
from docterella.pydantic.components import ReturnValue
from docterella.pydantic.components import FunctionDocstring
from docterella.pydantic.components import ClassDocstring

class FunctionAssessment(BaseModel):
    summary_of_findings: str

    parameter_names_are_correct: bool
    parameter_types_are_correct: bool
    parameter_descriptions_are_correct: bool
    return_type_is_correct: bool

    corrected_function_docstring: FunctionDocstring

    @property
    def docstring(self):
        return self.corrected_function_docstring
    
class ClassAssessment(BaseModel):
    summary_of_findings: str

    parameter_names_are_correct: bool
    parameter_types_are_correct: bool
    parameter_descriptions_are_correct: bool

    corrected_class_docstring: ClassDocstring

    @property
    def docstring(self):
        return self.corrected_class_docstring



