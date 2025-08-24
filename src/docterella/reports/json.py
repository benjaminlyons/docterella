
from typing import Generator
from docterella.results import ValidationResults

import json

class JSONReport:
    def __init__(self, results: Generator[ValidationResults]):
        self.results = results

        self.json = self.generate()

    def generate(self):
        return json.dumps([r.to_dict() for r in self.results], indent=4)

    def to_file(self, filename: str):
        with open(filename, 'w') as f:
            print(self.json, file=f)

