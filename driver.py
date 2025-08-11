import sys

from docterella.agent import ValidationAgent
from docterella.connections.ollama_connection import OllamaConnection
from docterella.connections.anthropic_connection import AnthropicConnection
from docterella.parsers.file_parser import FileParser
from docterella.parsers.sequence_parser import SequenceParser
from docterella.components.metadata import ClassMetadata
from docterella.components.metadata import FunctionMetadata

def main():
    filename = sys.argv[1]

    connection = AnthropicConnection("claude-3-haiku-20240307")

    # connection = OllamaConnection("llama3.1:8b-instruct-q8_0")
    # connection = OllamaConnection("deepseek-r1:14B")

    # connection = OllamaConnection("mistral:7b-instruct-q8_0")
    # connection = OllamaConnection("gemma3:12b-it-qat")
    # connection = OllamaConnection("codellama:13b-instruct")
    # connection = OllamaConnection("mistral-nemo:12b-instruct-2407-q6_K")

    validator = ValidationAgent(connection)
    parser = FileParser(filename)
    
    for result in validate_sequence(parser, validator):
        print(result)

    
def validate_sequence(parser: SequenceParser, validator: ValidationAgent):
    for node in parser.parse():
        if isinstance(node, ClassMetadata):
            yield validator.validate_class(node)
        
        if isinstance(node, FunctionMetadata):
            yield validator.validate_function(node)

if __name__ == "__main__":
    main()

