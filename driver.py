import sys

from docterella.agent import ValidationAgent
from docterella.connections.ollama_connection import OllamaConnection
from docterella.parsers.file_parser import FileParser
from docterella.parsers.sequence_parser import SequenceParser


def main():
    filename = sys.argv[1]

    connection = OllamaConnection("llama3.1:8b-instruct-q8_0")

    validator = ValidationAgent(connection)
    parser = FileParser(filename)

    
    for result in validate_sequence(parser, validator):
        print(result)

    
def validate_sequence(parser: SequenceParser, validator: ValidationAgent):
    for function in parser.parse():
        yield validator.validate_function(function)

if __name__ == "__main__":
    main()

