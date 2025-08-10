import ast

from docterella.parsers.sequence_parser import SequenceParser
from docterella.parsers.function_parser import parse_function

class FileParser(SequenceParser):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def parse(self):
        file = self.__read_file()

        parsed_content = ast.parse(file)

        for node in ast.walk(parsed_content):
            if not isinstance(node, ast.FunctionDef):
                continue

            yield parse_function(node)

    def __read_file(self):
        with open(self.filepath) as f:
            content = f.read()

        return content

    
