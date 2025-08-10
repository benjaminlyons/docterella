from docterella.components.assessment import DocstringAssessment
from docterella.parsers.function_parser import FunctionMetadata

import json

class ValidationResults:
    def __init__(self, metadata: FunctionMetadata, assessment: DocstringAssessment):
        self.metadata = metadata
        self.assessment = assessment

    def to_dict(self):
        return {
            "metadata": self.metadata.model_dump(),
            "assessment": self.assessment.model_dump()
        }
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
    
    def __str__(self):
        return self.to_json()

