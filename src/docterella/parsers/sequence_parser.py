from abc import ABC
from abc import abstractmethod

class SequenceParser(ABC):
    @abstractmethod
    def parse(self):
        """Generates sequence of ast nodes that should be validated"""
        pass