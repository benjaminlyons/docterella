from pydantic import BaseModel

from abc import ABC
from abc import abstractmethod
from docterella.pydantic.components import Argument
from docterella.pydantic.components import ReturnValue
from docterella.pydantic.components import FunctionDocstring
from docterella.pydantic.components import ClassDocstring

class Assessment(BaseModel, ABC):
    summary_of_findings: str

    parameter_names_are_correct: bool
    parameter_types_are_correct: bool
    parameter_descriptions_are_correct: bool

    
    @property
    @abstractmethod
    def docstring(self):
        pass

class FunctionAssessment(Assessment):
    return_type_is_correct: bool

    corrected_function_docstring: FunctionDocstring

    @property
    def docstring(self):
        return self.corrected_function_docstring
    
class ClassAssessment(Assessment):

    corrected_class_docstring: ClassDocstring

    @property
    def docstring(self):
        return self.corrected_class_docstring

