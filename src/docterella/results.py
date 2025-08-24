from docterella.pydantic.assessments import Assessment
from docterella.pydantic.metadata import Metadata

import json

class ValidationResults:
    def __init__(
        self, metadata: Metadata, assessment: Assessment
    ):
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
    
    def get_type(self) -> str:
        return self.metadata.type

    @property
    def docstring(self):
        return self.assessment.docstring