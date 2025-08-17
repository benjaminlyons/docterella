from docterella.prompts.function_prompt import FUNCTION_PROMPT
from docterella.prompts.class_prompt import CLASS_PROMPT
from docterella.prompts.cot_class_prompt import COT_CLASS_PROMPT
from docterella.prompts.cot_function_prompt import COT_FUNCTION_PROMPT

from docterella.objects.base_assessment import BaseFunctionDocstringAssessment
from docterella.objects.base_assessment import BaseClassDocstringAssessment
from docterella.objects.cot_assessment import CoTClassDocstringAssessment
from docterella.objects.cot_assessment import CoTFunctionDocstringAssessment

class PromptConfig:
    def __init__(self, prompt, output):
        self.prompt = prompt
        self.output = output

FUNCTION_PROMPT_CONFIG = PromptConfig(FUNCTION_PROMPT, BaseFunctionDocstringAssessment)
COT_FUNCTION_PROMPT_CONFIG = PromptConfig(COT_FUNCTION_PROMPT, CoTFunctionDocstringAssessment)

CLASS_PROMPT_CONFIG = PromptConfig(CLASS_PROMPT, BaseClassDocstringAssessment)
COT_CLASS_PROMPT_CONFIG = PromptConfig(COT_CLASS_PROMPT, CoTClassDocstringAssessment)

