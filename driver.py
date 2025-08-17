import sys

from docterella.validators.agent import ValidationAgent
from docterella.parsers.file_parser import FileParser
from docterella.connections.ollama_connection import OllamaConnection
from docterella.connections.anthropic_connection import AnthropicConnection

from docterella.runner import Runner
from docterella.converters.numpy import NumpyStyleBuilder

def main():
    filename = sys.argv[1]

    connection = AnthropicConnection("claude-3-5-haiku-20241022")
    #connection = OllamaConnection("llama3.1:8b-instruct-q8_0")

    validator = ValidationAgent(connection)
    parser = FileParser(filename)
    
    runner = Runner(parser, validator)

    results = runner.validate_sequence()

    nsb = NumpyStyleBuilder()

    for res in results:
        print(res)
        print(nsb.to_docstring(res))

if __name__ == "__main__":
    main()


