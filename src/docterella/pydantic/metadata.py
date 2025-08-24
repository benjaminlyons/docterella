import ast

from pydantic import BaseModel, ConfigDict
from abc import ABC
from typing import Optional
from typing import ClassVar
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
    type: ClassVar[str] = MetaDataTypes.FUNCTION_TYPE

class ClassMetadata(Metadata):
    type: ClassVar[str] = MetaDataTypes.CLASS_TYPE

    docstring: Optional[str] = ""
    constructor: FunctionMetadata