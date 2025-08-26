from pydantic import BaseModel
from abc import ABC

from docterella.pydantic.components import FunctionDocstring
from docterella.pydantic.components import ClassDocstring

class StreamlinedFunctionReasoning(BaseModel):
    signature_params: List[str]
    docstring_params: List[str]
    missing_params_from_docstring: List[str]
    missing_params_from_implementation: List[str]
    extra_params_in_docstring: List[str]
    params_with_correct_descriptions: List[str]
    return_types_in_signature: List[str]
    return_types_in_docstring: List[str]

class StreamlinedClassReasoning(BaseModel):
    signature_params: List[str]
    docstring_params: List[str]
    missing_params_from_docstring: List[str]
    missing_params_from_implementation: List[str]
    extra_params_in_docstring: List[str]
    params_with_correct_descriptions: List[str]

class StreamlinedAssessment(BaseModel, ABC):
    params_match_signature: bool
    params_match_implementation: bool
    
    @property
    @abstractmethod
    def docstring(self):
        pass


class FunctionStreamlinedAssessment(StreamlinedAssessment):
    reasoning: StreamlinedFunctionReasoning

    returns_match_signature: bool
    returns_match_implementation: bool

    correct_docstring: FunctionDocstring

    @property
    def docstring(self):
        return self.corrected_docstring


class ClassStreamlinedAssessment(StreamlinedAssessment):
    reasoning: StreamlinedClassReasoning
    correct_docstring: ClassDocstring

    @property
    def docstring(self):
        return self.correct_class_docstring

