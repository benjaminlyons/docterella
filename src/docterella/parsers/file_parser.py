import ast

from docterella.parsers.sequence_parser import SequenceParser
from docterella.pydantic.metadata import ClassMetadata
from docterella.pydantic.metadata import FunctionMetadata

from typing import List

class FileParser(SequenceParser):
    def __init__(self, filepath: str, excluded_names: List[str] = None):
        self.filepath = filepath
        
        if excluded_names is None:
            self.excluded_names = ["__init__"]

    def parse(self):
        file = self.__read_file()

        parsed_content = ast.parse(file)

        for node in ast.walk(parsed_content):
            if isinstance(node, ast.FunctionDef) and node.name not in self.excluded_names:
                yield FunctionMetadata.from_ast(node, self.filepath)

            if isinstance(node, ast.ClassDef) and node.name not in self.excluded_names:
                yield ClassMetadata.from_ast(node, self.filepath)

    def __read_file(self):
        with open(self.filepath) as f:
            content = f.read()

        return content
    
