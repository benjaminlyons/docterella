from docterella.pydantic.assessments import FunctionAssessment
from docterella.pydantic.assessments import ClassAssessment

from docterella.pydantic.reasoning import FunctionReasoning
from docterella.pydantic.reasoning import ClassReasoning

from pydantic import BaseModel

class _FunctionReasoningAssessment(BaseModel):
    reasoning: FunctionReasoning

class _ClassReasoningAssessment(BaseModel):
    reasoning: ClassReasoning

# It is very important the reasoning outputs come first, and this order appears
# to ensure that
class CoTFunctionAssessment(FunctionAssessment, _FunctionReasoningAssessment):
    pass


class CoTClassAssessment(ClassAssessment, _ClassReasoningAssessment):
    pass

