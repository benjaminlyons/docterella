from typing import List
from pydantic import BaseModel

class FunctionReasoning(BaseModel):
    signature_parameters: List[str]
    docstring_parameters: List[str]
    missing_params_from_docstring: List[str]
    extra_params_in_docstring: List[str]
    incorrect_param_descriptions: List[str]
    return_type_matches: bool

class ClassReasoning(BaseModel):
    signature_parameters: List[str]
    docstring_parameters: List[str]
    missing_params_from_docstring: List[str]
    extra_params_in_docstring: List[str]
    incorrect_param_descriptions: List[str]

class BaseFunctionReasoningAssessment(BaseModel):
    reasoning: FunctionReasoning

class BaseClassReasoningAssessment(BaseModel):
    reasoning: ClassReasoning
