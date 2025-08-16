import sys

from docterella.validators.agent import ValidationAgent
from docterella.parsers.file_parser import FileParser

from docterella.runner import Runner

def main():
    filename = sys.argv[1]

    connection = AnthropicConnection("claude-3-5-haiku-20241022")

    # connection = OllamaConnection("llama3.1:8b-instruct-q8_0")
    # connection = OllamaConnection("mistral:7b-instruct-q8_0")
    # connection = OllamaConnection("gemma3:12b-it-qat")

    validator = ValidationAgent(connection)
    parser = FileParser(filename)
    
    runner = Runner(parser, validator)

    results = runner.validate_sequence()

if __name__ == "__main__":
    main()


