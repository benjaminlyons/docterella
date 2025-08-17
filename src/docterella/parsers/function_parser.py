import ast
import astor

from docterella.objects.metadata import FunctionMetadata

def parse_function(node: ast.FunctionDef) -> FunctionMetadata:
    if not isinstance(node, ast.FunctionDef):
        raise TypeError("Argument `node` must be type ast.FunctionDef")

    return FunctionMetadata(
        name=node.name,
        lineno=node.lineno,
        source=astor.to_source(node),
    )