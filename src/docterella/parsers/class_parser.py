import ast
import astor
from docterella.pydantic.metadata import ClassMetadata
from docterella.parsers.function_parser import parse_function

def parse_class(node: ast.ClassDef) -> ClassMetadata:
    
    docstring = ast.get_docstring(node)

    constructor = get_constructor(node)

    return ClassMetadata(
        name=node.name,
        lineno=node.lineno,
        source=astor.to_source(node),
        constructor=constructor,
        docstring=docstring,
    )

def get_constructor(node: ast.ClassDef):
    for child in ast.iter_child_nodes(node):
        if not isinstance(child, ast.FunctionDef):
            continue

        if child.name == "__init__":
            return parse_function(child)
        
    return None
