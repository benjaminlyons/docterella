import sys

from docterella.agents.base import ValidationAgent
from docterella.parsers.file_parser import FileParser
from docterella.connections.ollama_connection import OllamaConnection
from docterella.connections.anthropic_connection import AnthropicConnection

from docterella.runner import Runner
from docterella.docstrings.numpy import NumpyStyleBuilder
from docterella.docstrings.google import GoogleStyleBuilder
from docterella.agents.config import AgentConfigFactory

from docterella.reports.json import JSONReport

def main():
    filename = sys.argv[1]

    # connection = AnthropicConnection("claude-3-5-haiku-20241022")
    connection = OllamaConnection("llama3.1:8b-instruct-q8_0")
    # connection = OllamaConnection("phi4-mini:latest")
   # connection = OllamaConnection("phi4-mini-reasoning:3.8b")

    validator = ValidationAgent(connection, AgentConfigFactory.create('basic'))
    parser = FileParser(filename)
    
    runner = Runner(parser, validator)

    results = runner.validate_sequence()

    nsb = NumpyStyleBuilder()
    gsb = GoogleStyleBuilder()

    report = JSONReport(results)

    report.to_file("test_output.json")

    # print(nsb.to_docstring(res))
    # print(gsb.to_docstring(res))

if __name__ == "__main__":
    main()


