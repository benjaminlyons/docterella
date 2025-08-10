import ast
import astor

from pydantic import BaseModel

class FunctionMetadata(BaseModel):
    function_name: str
    lineno: int
    source: str

def parse_function(node: ast.FunctionDef):
    if not isinstance(node, ast.FunctionDef):
        raise TypeError("Argument `node` must be type ast.FunctionDef")

    return FunctionMetadata(
        function_name=node.name,
        lineno=node.lineno,
        source=astor.to_source(node),
    )