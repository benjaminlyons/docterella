from docterella.docstrings.docstring_builder import DocstringBuilder

class NumpyStyleBuilder(DocstringBuilder):
    def __init__(self):
        super().__init__(
            argument_listing_format="{name}: {datatype}\n\t{description}",
            return_listing_format="{datatype}:\n\t{description}",
        )

    def _assemble(self, description: str, arguments: str, return_vals: str = None):
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

    