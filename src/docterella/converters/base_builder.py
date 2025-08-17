from abc import ABC
from abc import abstractmethod

from docterella.components.assessment import FunctionDocstring
from docterella.components.assessment import ClassDocstring

from typing import List
from docterella.components.assessment import Argument
from docterella.components.assessment import ReturnValue
from docterella.components.results import ValidationResults

from docterella.components.metadata import MetaDataTypes

class BaseBuilder(ABC):
    def __init__(self, argument_listing_format: str, return_listing_format: str):
        self.argument_listing_format = argument_listing_format
        self.return_listing_format = return_listing_format

    def to_docstring(self, result: ValidationResults):
        if result.get_type() == MetaDataTypes.FUNCTION_TYPE:
            return self.build_function_docstring(result.docstring)
        elif result.get_type() == MetaDataTypes.CLASS_TYPE:
            return self.build_class_docstring(result.docstring)
        else:
            raise ValueError(f"The result type {result.get_type()} is unknown")

    def build_function_docstring(self, docs: FunctionDocstring):
        description = docs.correct_function_description
        arguments = self._build_arguments_listing(docs.correct_function_arguments)
        return_vals = self._build_return_vals_listing(docs.correct_function_return_values)
        return self.assemble(description, arguments, return_vals)

    def build_class_docstring(self, docs: ClassDocstring):
        description = docs.correct_class_description
        arguments = self._build_arguments_listing(docs.correct_class_arguments)
        return self.assemble(description, arguments)
        
    @abstractmethod
    def assemble(self, description, arguments, return_vals = None):
        pass

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

