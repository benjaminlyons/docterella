from pydantic import BaseModel

from typing import List
from typing import Dict
from typing import Optional

class Argument(BaseModel):
    # name of the argument
    name: str

    # string representation of the argument type (e.g., bool)
    data_type: str

    # description of the argument
    description: str

class ReturnValue(BaseModel):
    data_type: str
    description: str

class FunctionDocstring(BaseModel):
    # one line description of the function 
    correct_function_description: str

    # list of expected docstring arguments
    correct_function_arguments: List[Argument]

    correct_function_return_values: List[ReturnValue]

class ClassDocstring(BaseModel):
    correct_class_description: str
    correct_class_arguments: List[Argument]