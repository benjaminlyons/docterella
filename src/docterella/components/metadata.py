import ast

from pydantic import BaseModel, ConfigDict
from abc import ABC
from typing import Optional
from enum import Enum

class MetaDataTypes(Enum):
    FUNCTION_TYPE  = "function"
    CLASS_TYPE = "class"

class Metadata(BaseModel, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    lineno: int
    source: str

class FunctionMetadata(Metadata):
    type = MetaDataTypes.FUNCTION_TYPE

class ClassMetadata(Metadata):
    docstring: Optional[str] = ""
    constructor: FunctionMetadata

    type = MetaDataTypes.CLASS_TYPE