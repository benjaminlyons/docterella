
from enum import Enum

from docterella.converters.base_builder import BaseBuilder

class DocstringStyles(Enum):
    GOOGLE = "google"
    NUMPY = "numpy"

class NumpyStyleBuilder(BaseBuilder):
    def __init__(self):
        super().__init__(
            argument_listing_format="{name}: {datatype}\n\t{description}",
            return_listing_format="{datatype}:\n\t{description}",
        )

    def assemble(self, description, arguments, return_vals = None):
        output = f"\"\"\"{description}\n"

        if arguments:
            output += f"\nParameters\n"
            output +=    "----------\n"
            output += f"{arguments}\n"

        if return_vals:
            output += f"\nReturns\n"
            output +=    "-------\n"
            output += f"{return_vals}\n"

        output += "\"\"\""

        return output

    