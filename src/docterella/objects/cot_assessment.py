
from docterella.objects.components import FunctionDocstring
from docterella.objects.components import ClassDocstring

from docterella.objects.base_assessment import BaseFunctionDocstringAssessment
from docterella.objects.base_assessment import BaseClassDocstringAssessment

from docterella.objects.reasoning import BaseClassReasoningAssessment
from docterella.objects.reasoning import BaseFunctionReasoningAssessment

class CoTFunctionDocstringAssessment(BaseFunctionReasoningAssessment, BaseFunctionDocstringAssessment):
    pass


class CoTClassDocstringAssessment(BaseClassReasoningAssessment, BaseClassDocstringAssessment):
    pass

