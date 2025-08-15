from docterella.connections.base_connection import BaseConnection
from docterella.connections.anthropic_connection import AnthropicConnection
from docterella.connections.ollama_connection import OllamaConnection
from docterella.agent import ValidationAgent
from docterella.parsers.file_parser import FileParser
from docterella.parsers.sequence_parser import SequenceParser
from docterella.components.metadata import ClassMetadata
from docterella.components.metadata import FunctionMetadata
from docterella.components.results import ValidationResults
from docterella.components.assessment import ClassDocstringAssessment
from docterella.components.assessment import FunctionDocstringAssessment
from docterella.components.assessment import ClassDocstring
from docterella.components.assessment import FunctionDocstring
from docterella.components.assessment import ReturnValue

import json
import pandas as pd

from typing import List
from docterella.components.assessment import Argument

import dataclasses
from dataclasses import dataclass


def compare_assessments(assessment, expected_assessment):
    act_dict = assessment.model_dump()

    results_dict = {}
    for key in act_dict:
        act_val = assessment.__dict__[key]
        exp_val = expected_assessment.__dict__[key]

        if isinstance(act_val, ClassDocstring):
            results_dict.update(compare_class_docstring(act_val, exp_val))
        elif isinstance(act_val, FunctionDocstring):
            results_dict.update(compare_function_docstring(act_val, exp_val))
        else:
            results_dict[key] = act_val == exp_val

    return results_dict

def compare_class_docstring(cd1: ClassDocstring, cd2: ClassDocstring):
    return dataclasses.asdict(
        compare_all_arguments(
            cd1.correct_class_arguments, 
            cd2.correct_class_arguments,
        )
    )

@dataclass
class DocstringArgumentsComparison:
    arg_name: int = 0
    arg_data_type: int = 0
    arg_description: int = 0
    num_args: int = 0

@dataclass
class ArgumentComparison:
    name: int
    data_type: int
    description: int

@dataclass
class ReturnValueComparison:
    ret_data_type: int
    num_rets: bool

def compare_all_arguments(args1: List[Argument], args2: List[Argument]):
    arg_comp = DocstringArgumentsComparison(
        arg_name=0,
        arg_data_type=0,
        arg_description=0,
        num_args=len(args1) == len(args2)
    )

    total = 0
    for a1, a2 in zip(args1, args2):
        comp = compare_argument(a1, a2)

        arg_comp.arg_name += comp.name
        arg_comp.arg_data_type += comp.data_type
        arg_comp.arg_description += comp.description

        total += 1

    if total != 0:
        arg_comp.arg_name /= total
        arg_comp.arg_data_type /= total
        arg_comp.arg_description /= total

    return arg_comp


def compare_argument(arg1: Argument, arg2: Argument) -> ArgumentComparison:
    return ArgumentComparison(
        name=arg1.name == arg2.name,
        data_type=arg1.data_type == arg2.data_type,
        description=arg1.description == arg2.description,
    )

def compare_function_docstring(fd1: FunctionDocstring, fd2: FunctionDocstring):
    return {
        **dataclasses.asdict(compare_all_arguments(
            fd1.correct_function_arguments, 
            fd2.correct_function_arguments,
        )),
        **dataclasses.asdict(compare_return_values(
            fd1.correct_function_return_values, 
            fd2.correct_function_return_values
        ))
    }


def compare_return_values(ret1: List[ReturnValue], ret2: List[ReturnValue]):
    return ReturnValueComparison(
        ret_data_type=sum(r1.data_type == r2.data_type for r1, r2 in zip(ret1, ret2)), 
        num_rets=len(ret1) == len(ret2)
    )

def validate_sequence(parser: SequenceParser, validator: ValidationAgent):
    for node in parser.parse():
        if isinstance(node, ClassMetadata):
            yield validator.validate_class(node)
        
        if isinstance(node, FunctionMetadata):
            yield validator.validate_function(node)

def benchmark(model: str):

    """
    Benchmarks a model by comparing its output to expected responses.

    Args:
        model (str): The name of the model to benchmark.
    """
    functions_path = "tests/data/functions.py"
    functions_response_path = "tests/data/function_responses.json"

    class_path = "tests/data/class.py"
    class_response_path = "tests/data/class_responses.json"

    paths = [
        ("function", functions_path, functions_response_path),
        ("class", class_path, class_response_path),
    ]

    connection = load_model(model)

    metrics = []
    responses = ""
    for case, input_path, response_path in paths:
        metric, response = _benchmark_helper(connection, input_path, response_path)
        metric = metric.rename({col: f"{col}_{case}" for col in metric.index})
        metrics.append(metric)

    metrics_series = pd.concat(metrics)

    save_model_response(model, response, metrics_series)

def load_model(model):
    """
    Loads a model based on the provided name.

    Args:
        model (str): The name of the model to load.

    Returns:
        BaseConnection: The loaded model connection.
    """
    if "claude" in model:
        return AnthropicConnection(model)
    else:
        return OllamaConnection(model)

def _benchmark_helper(
    connection: BaseConnection, 
    input_file_path: str, 
    response_file_path: str
):
    """
    Helper function for benchmarking a model.

    Args:
        connection (BaseConnection): The model connection to use.
        input_file_path (str): The path to the input file containing metadata nodes.
        response_file_path (str): The path to the expected responses file.

    Returns:
        pd.Series, str: The metrics series and the generated responses.
    """
    with open(response_file_path, 'r') as f:
        expected_response_dict = json.load(f)
    
    validator = ValidationAgent(connection)
    parser = FileParser(input_file_path)

    metrics = []
    responses = []
    for result in validate_sequence(parser, validator):
        expected = expected_response_dict[result.metadata.name]

        if isinstance(result.assessment, ClassDocstringAssessment):
            expected_assessment = ClassDocstringAssessment.model_validate(expected)
        else:
            expected_assessment = FunctionDocstringAssessment.model_validate(expected)

        assessment = result.assessment

        check = compare_assessments(assessment, expected_assessment)
        check["name"] = result.metadata.name

        metrics.append(check)
        responses.append(str(result))

    metrics_series = pd.DataFrame(metrics).mean(numeric_only=True)

    return metrics_series, responses

def save_model_response(model: str, response: str, metrics: pd.Series, base_path = "tests/data/results/"):
    """
    Saves the model response and metrics to files.

    Args:
        model (str): The name of the model.
        response (str): The generated responses.
        metrics (pd.Series): The metrics series.
        base_path (str): The base path for saving the files.
    """
    model_path = base_path + model_to_path(model)

    response_path = f"{model_path}_response.json"
    metric_path = f"{model_path}_metric.json"

    with open(response_path, 'w') as f:
        for o in response:
            print(o, file=f)

    with open(metric_path, 'w') as f:
        json.dump(metrics.to_dict(), f, indent=4)

def model_to_path(model: str):
    """
    Converts a model name to a path format.

    Args:
        model (str): The model name.

    Returns:
        str: The converted path.
    """
    punctuation = [":", "-", "."]

    translation = str.maketrans({p: "_" for p in punctuation})

    return model.translate(translation)

def main():
    """
    Main function to run the benchmarking process.

    This function sets up and runs the benchmarking process using a specified model.
    """
    models = [
        "llama3.1:8b-instruct-q8_0",
        "phi4:latest",
        "phi3:14b-medium-128k-instruct-q4_K_M",
        "claude-3-5-haiku-20241022",
        "mistral:7b-instruct-q8_0",
        "gemma3:12b-it-qat",
        "phi4-mini-reasoning:3.8b",
    ]

    for model in models: 
        print(f"Running benchmarks for {model}")
        benchmark(model)
        
if __name__ == "__main__":
    main()
