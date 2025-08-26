import ast
import astor
from pydantic import BaseModel, ConfigDict
from abc import ABC
from typing import Optional
from typing import ClassVar
from typing import Dict

from enum import Enum

class MetaDataTypes(Enum):
    FUNCTION_TYPE  = "function"
    CLASS_TYPE = "class"

class Metadata(BaseModel, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # str describing a path to the source file (could be filepath or other identifier)
    source_path: Optional[str] = None
    name: str
    lineno: int
    end_lineno: int
    col_offset: int
    end_col_offset: int

    source_code: str

    @staticmethod
    def kv_from_ast(node: ast.AST) -> Dict:
        return {
            "name": node.name,
            "lineno": node.lineno,
            "end_lineno": node.end_lineno,
            "col_offset": node.col_offset,
            "end_col_offset": node.end_col_offset,
            "source_code": astor.to_source(node),
        }
    
    def to_dict(self):
        return self.model_dump()

class FunctionMetadata(Metadata):
    type: ClassVar[str] = MetaDataTypes.FUNCTION_TYPE

    @staticmethod
    def from_ast(node: ast.FunctionDef, source_path: str = None):
        if not isinstance(node, ast.FunctionDef):
            raise TypeError("Argument `node` must be type ast.FunctionDef")
    
        return FunctionMetadata(source_path=source_path, **Metadata.kv_from_ast(node))


class ClassMetadata(Metadata):
    type: ClassVar[str] = MetaDataTypes.CLASS_TYPE

    docstring: Optional[str] = ""
    constructor: FunctionMetadata

    @staticmethod
    def from_ast(node: ast.ClassDef, source_path: str = None):
        if not isinstance(node, ast.ClassDef):
            raise TypeError("Argument `node` must be type ast.ClassDef")
        
        docstring = ast.get_docstring(node)

        constructor = ClassMetadata.__get_constructor(node, source_path)

        return ClassMetadata(
            source_path=source_path,
            **Metadata.kv_from_ast(node),
            constructor=constructor,
            docstring=docstring,
        )
    
    @staticmethod
    def __get_constructor(node: ast.ClassDef, source_path: str = None):
        for child in ast.iter_child_nodes(node):
            if not isinstance(child, ast.FunctionDef):
                continue

            if child.name == "__init__":
                return FunctionMetadata.from_ast(child, source_path)
            
        return None
