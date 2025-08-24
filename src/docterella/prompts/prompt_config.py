from docterella.prompts.function_prompt import FUNCTION_PROMPT
from docterella.prompts.class_prompt import CLASS_PROMPT
from docterella.prompts.cot_class_prompt import COT_CLASS_PROMPT
from docterella.prompts.cot_function_prompt import COT_FUNCTION_PROMPT
from docterella.prompts.streamlined_class_prompt import OPTIMIZED_CLASS_PROMPT
from docterella.prompts.streamlined_function_prompt import OPTIMIZED_FUNCTION_PROMPT

from docterella.pydantic.assessments import FunctionAssessment
from docterella.pydantic.assessments import ClassAssessment
from docterella.pydantic.cot_assessment import CoTClassAssessment
from docterella.pydantic.cot_assessment import CoTFunctionAssessment
from collections import namedtuple

PromptConfig = namedtuple("PromptConfig", ["prompt", "output"])

FUNCTION_PROMPT_CONFIG = PromptConfig(FUNCTION_PROMPT, FunctionAssessment)
CLASS_PROMPT_CONFIG = PromptConfig(CLASS_PROMPT, ClassAssessment)

COT_FUNCTION_PROMPT_CONFIG = PromptConfig(COT_FUNCTION_PROMPT, CoTFunctionAssessment)
COT_CLASS_PROMPT_CONFIG = PromptConfig(COT_CLASS_PROMPT, CoTClassAssessment)

STREAMLINED_FUNCTION_PROMPT_CONFIG = PromptConfig(OPTIMIZED_FUNCTION_PROMPT, CoTFunctionAssessment)
STREAMLINED_CLASS_PROMPT_CONFIG = PromptConfig(OPTIMIZED_CLASS_PROMPT, CoTClassAssessment)
