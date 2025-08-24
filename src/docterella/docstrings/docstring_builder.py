from abc import ABC
from abc import abstractmethod

from docterella.pydantic.assessments import FunctionDocstring
from docterella.pydantic.assessments import ClassDocstring

from typing import List
from docterella.pydantic.assessments import Argument
from docterella.pydantic.assessments import ReturnValue
from docterella.results import ValidationResults

from docterella.pydantic.metadata import MetaDataTypes

class DocstringBuilder(ABC):
    """Base class for generating docstrings based on model outputs
    
    Parameters
    ----------
    argument_listing_format: str
        The format string to use for assembling each argument in the docstring.
        This string is used with the `.format` method with the following
        keyword arguments:

            * name - argument name
            * datatype - argument datatype
            * description - argument description

        An example value is `{name}: {datatype}\n\t{description}`

    return_listing_format: str
        The format string to use for assembling the return values in a docstring
        This string is used with the `.format` method with the following 
        keyword arguments:

            * datatype - the return value's datatype
            * description - a description of the return value

        An example value for `return_listing_format` is 
        `{datatype}:\n\t{description}`
    """
    def __init__(self, argument_listing_format: str, return_listing_format: str):
        self.argument_listing_format = argument_listing_format
        self.return_listing_format = return_listing_format

    def to_docstring(self, result: ValidationResults):
        if result.get_type() == MetaDataTypes.FUNCTION_TYPE:
            return self._build_function_docstring(result.docstring)
        elif result.get_type() == MetaDataTypes.CLASS_TYPE:
            return self._build_class_docstring(result.docstring)
        else:
            raise ValueError(f"The result type {result.get_type()} is unknown")

    def _build_function_docstring(self, docs: FunctionDocstring):
        description = docs.correct_function_description
        arguments = self._build_arguments_listing(docs.correct_function_arguments)
        return_vals = self._build_return_vals_listing(docs.correct_function_return_values)
        return self._assemble(description, arguments, return_vals)

    def _build_class_docstring(self, docs: ClassDocstring):
        description = docs.correct_class_description
        arguments = self._build_arguments_listing(docs.correct_class_arguments)
        return self._assemble(description, arguments)
        

    def _build_arguments_listing(self, args: List[Argument]) -> str:
        return "\n".join([
            self.argument_listing_format.format(
                name=a.name, 
                datatype=a.data_type, 
                description=a.description
            ) 
            for a in args
        ])


    def _build_return_vals_listing(self, rets: List[ReturnValue]) -> str:
        return "\n".join([
            self.return_listing_format.format(
                datatype=r.data_type,
                description=r.description
            )
            for r in rets
        ])
    
    @abstractmethod
    def _assemble(self, description: str, arguments: str, return_vals = None):
        pass

