import ast

from pydantic import BaseModel, ConfigDict
from abc import ABC
from typing import Optional

class Metadata(BaseModel, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    lineno: int
    source: str

class FunctionMetadata(Metadata):
    pass

class ClassMetadata(Metadata):
    docstring: Optional[str] = ""
    constructor: FunctionMetadata
