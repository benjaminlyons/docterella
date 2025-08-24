from docterella.parsers.sequence_parser import SequenceParser
from docterella.agents.base import ValidationAgent
from docterella.pydantic.metadata import ClassMetadata
from docterella.pydantic.metadata import FunctionMetadata

class Runner:
    def __init__(self, parser: SequenceParser, agent: ValidationAgent):
        self.parser = parser
        self.agent = agent

    def validate_sequence(self):
        for node in self.parser.parse():
            if isinstance(node, ClassMetadata):
                yield self.agent.validate_class(node)

            if isinstance(node, FunctionMetadata):
                yield self.agent.validate_function(node)

    def run(self):
        return [res for res in self.validate_sequence()]