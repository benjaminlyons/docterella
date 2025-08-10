import ast

from docterella.parsers.sequence_parser import SequenceParser
from docterella.parsers.function_parser import parse_function
from docterella.parsers.class_parser import parse_class

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
                yield parse_function(node)

            if isinstance(node, ast.ClassDef):
                yield parse_class(node)

    def __read_file(self):
        with open(self.filepath) as f:
            content = f.read()

        return content

    
