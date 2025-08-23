from docterella.prompts.prompt_config import PromptConfig
from docterella.prompts.prompt_config import COT_CLASS_PROMPT_CONFIG
from docterella.prompts.prompt_config import CLASS_PROMPT_CONFIG
from docterella.prompts.prompt_config import FUNCTION_PROMPT_CONFIG
from docterella.prompts.prompt_config import COT_FUNCTION_PROMPT_CONFIG
from docterella.prompts.prompt_config import STREAMLINED_FUNCTION_PROMPT_CONFIG
from docterella.prompts.prompt_config import STREAMLINED_CLASS_PROMPT_CONFIG

class AgentConfig:
    def __init__(self, func: PromptConfig, cls: PromptConfig):
        self.func = func
        self.cls = cls

    @property
    def function_prompt(self):
        return self.func.prompt
    
    @property
    def class_prompt(self):
        return self.cls.prompt
    
    @property
    def function_output(self):
        return self.func.output
    
    @property
    def class_output(self):
        return self.cls.output
    

class BasicConfig(AgentConfig):
    def __init__(self):
        super().__init__(FUNCTION_PROMPT_CONFIG, CLASS_PROMPT_CONFIG)

class ReasoningConfig(AgentConfig):
    def __init__(self):
        super().__init__(COT_FUNCTION_PROMPT_CONFIG, COT_CLASS_PROMPT_CONFIG)

class StreamlinedConfig(AgentConfig):
    def __init__(self):
        super().__init__(STREAMLINED_FUNCTION_PROMPT_CONFIG, STREAMLINED_CLASS_PROMPT_CONFIG)

class AgentConfigFactory:
    @staticmethod
    def create(style: str = None) -> AgentConfig:
        if style == "basic" or style is None:
            return BasicConfig()
        elif style == "reasoning":
            return ReasoningConfig()
        elif style == "streamlined":
            return StreamlinedConfig()
        else:
            raise ValueError(f"Unknown agent configuration style: {style}")