from docterella.converters.base_builder import BaseBuilder

class GoogleStyleBuilder(BaseBuilder):
    def __init__(self):
        super().__init__(
            argument_listing_format="\t{name} ({datatype}) : {description}",
            return_listing_format="\t{datatype} : {description}"
        )

    def assemble(self, description, arguments, return_vals=None):
        output = f"\"\"\"{description}\n"

        if arguments:
            output += f"\nArgs:\n"
            output += f"{arguments}\n"

        if return_vals:
            output += f"\nReturns:\n"
            output += f"{return_vals}\n"
        
        output += "\"\"\""

        return output