from pydantic import BaseModel

class FunctionMetadata(BaseModel):
    name: str
    lineno: int
    source: str
