"""Benchmarking script for evaluating docstring validation model performance.

This script provides comprehensive benchmarking functionality for testing different
LLM models on docstring validation tasks. It compares model-generated assessments
against expected responses and generates detailed metrics for performance evaluation.

The benchmarking system supports multiple model providers (Anthropic, OpenAI, Ollama)
and different validation configurations (basic, reasoning, streamlined).
"""

import pandas as pd
import dataclasses
import json
import itertools

from dataclasses import dataclass
from typing import List

from docterella.connections.base_connection import BaseConnection
from docterella.connections.anthropic_connection import AnthropicConnection
from docterella.connections.ollama_connection import OllamaConnection
from docterella.connections.openai_connection import OpenaiConnection
from docterella.validators.base_agent import ValidationAgent
from docterella.parsers.file_parser import FileParser
from docterella.objects.base_assessment import BaseClassDocstringAssessment
from docterella.objects.base_assessment import BaseFunctionDocstringAssessment
from docterella.objects.base_assessment import ClassDocstring
from docterella.objects.base_assessment import FunctionDocstring
from docterella.objects.base_assessment import ReturnValue
from docterella.objects.base_assessment import Argument
from docterella.runner import Runner
from docterella.validators.config import StreamlinedConfig
from docterella.validators.config import ReasoningConfig
from docterella.validators.config import AgentConfig
from docterella.validators.config import AgentConfigFactory

from pydantic import BaseModel

from collections import defaultdict

from typing import Dict
import os

class ReturnValueComparison:
    """Compares return value specifications between actual and expected docstring assessments.
    
    This class evaluates whether the return types and counts match between two sets of
    return value specifications, typically from LLM-generated and expected responses.
    """
    
    def __init__(self, act_ret: List[ReturnValue], exp_ret: List[ReturnValue]):
        """Initialize comparison between two sets of return values.
        
        Parameters
        ----------
        act_ret : List[ReturnValue]
            Actual return values to compare.
        exp_ret : List[ReturnValue]
            Expected return values to compare against.
        """
        self.corrected_return_types_match = sum(r1.data_type == r2.data_type for r1, r2 in zip(exp_ret, act_ret))
        self.corrected_return_counts_match = len(act_ret) == len(exp_ret)

class ArgumentComparison:
    """Compares argument specifications between actual and expected docstring assessments.
    
    This class evaluates whether argument names, types, and descriptions match between
    two argument specifications, typically from LLM-generated and expected responses.
    """
    
    def __init__(self, arg1: Argument, arg2: Argument):
        """Initialize comparison between two argument specifications.
        
        Parameters
        ----------
        arg1 : Argument
            First argument to compare.
        arg2 : Argument
            Second argument to compare against.
        """
        self.corrected_names_match = arg1.name == arg2.name
        self.corrected_types_match = arg1.data_type == arg2.data_type
        self.corrected_descriptions_match = arg1.description == arg2.description

@dataclass
class FieldComparison:
    """Tracks field-level comparisons for aggregating benchmark metrics.
    
    This class maintains dictionaries to track comparison results and counts
    across different fields, enabling calculation of mean accuracy scores.
    """
    
    field_comp_dict: Dict = dataclasses.field(default_factory=lambda: defaultdict(int))
    field_count_dict: Dict = dataclasses.field(default_factory=lambda: defaultdict(int))

    def update(self, key, val1, val2):
        """Update comparison results for a specific field.
        
        Parameters
        ----------
        key : str
            The field name being compared.
        val1 : Any
            First value to compare.
        val2 : Any
            Second value to compare against.
        """
        self.field_comp_dict[key] = int(val1 == val2)
        self.field_count_dict[key] = 1

    def __add__(self, other):
        """Aggregate comparison results from another FieldComparison.
        
        Parameters
        ----------
        other : FieldComparison
            Another FieldComparison instance to merge with this one.
            
        Returns
        -------
        FieldComparison
            This instance with aggregated results.
        """
        fields = set(list(other.field_comp_dict.keys()) + list(self.field_comp_dict.keys()))

        for field in fields:
            self.field_comp_dict[field] += other.field_comp_dict[field]
            self.field_count_dict[field] += other.field_count_dict[field]

        return self

    def to_mean(self):
        """Convert aggregated comparison counts to mean accuracy scores in place"""
        for field in self.field_comp_dict:
            self.field_comp_dict[field] /= self.field_count_dict[field]
        return self

@dataclass
class DocstringComparison:
    """Comprehensive comparison metrics for docstring validation assessments.
    
    This class tracks multiple accuracy metrics across argument names, types,
    descriptions, return values, and other docstring elements for benchmarking
    LLM performance on docstring validation tasks.
    """
    
    corrected_names_match: int = 0
    corrected_types_match: int = 0
    corrected_descriptions_match: int = 0
    corrected_num_args_match: int = 0

    args_count = 0

    corrected_return_types_match: int = 0
    corrected_return_counts_match: int = 0

    rets_count = 0

    field_comparison: FieldComparison = dataclasses.field(default_factory=FieldComparison)

    def __add__(self, other):
        """Aggregate metrics from argument or return value comparisons.
        
        Parameters
        ----------
        other : ArgumentComparison, ReturnValueComparison, or DocstringComparison
            An instance to merge with this comparison.
                  
        Returns
        -------
        DocstringComparison
            This instance with updated metrics.
        """
        if isinstance(other, ArgumentComparison) or isinstance(other, DocstringComparison):
            self.corrected_names_match += int(other.corrected_names_match)
            self.corrected_types_match += int(other.corrected_types_match)
            self.corrected_descriptions_match += int(other.corrected_descriptions_match)
            self.args_count += 1

        if isinstance(other, ReturnValueComparison) or isinstance(other, DocstringComparison):
            self.corrected_return_counts_match += int(other.corrected_return_counts_match)
            self.corrected_return_types_match += int(other.corrected_return_types_match)
            self.rets_count += 1

        if isinstance(other, DocstringComparison):
            self.field_comparison += other.field_comparison
            self.corrected_num_args_match += int(other.corrected_num_args_match)
            self.args_count += other.args_count - 1
            self.rets_count += other.rets_count - 1

        return self

    def to_mean(self):
        """Convert aggregated counts to mean accuracy scores in place."""
        if self.args_count:
            self.corrected_names_match /= self.args_count
            self.corrected_types_match /= self.args_count
            self.corrected_descriptions_match /= self.args_count

        if self.rets_count:
            self.corrected_return_counts_match = self.rets_count
            self.corrected_return_types_match = self.rets_count


        self.field_comparison.to_mean()

        return self

    def to_dict(self):
        """Convert comparison metrics to dictionary format.
        
        Returns
        -------
        dict
            Dictionary representation of all comparison metrics.
        """

        output_dict = dataclasses.asdict(self)
        output_dict.update(**output_dict['field_comparison']["field_comp_dict"])

        del output_dict["field_comparison"]

        return output_dict

class TestCaseSuite:
    """Manages test cases for benchmarking docstring validation models.
    
    This class handles loading test input files and expected response data,
    providing a standardized interface for running benchmark comparisons
    against different validation models.
    """
    
    def __init__(
        self, 
        label: str, 
        input_path: str, 
        response_path: str, 
        ValidationClass: BaseModel,
    ):
        """Initialize a test case suite.
        
        Parameters
        ----------
        label : str
            Human-readable label for this test suite (e.g., 'function', 'class').
        input_path : str
            Path to the Python file containing test cases.
        response_path : str
            Path to JSON file with expected validation responses.
        ValidationClass : BaseModel
            Pydantic model class for validating responses.
        """
        self.label = label
        self.input_path  = input_path
        self.response_path = response_path
        self.ValidationClass = ValidationClass

        self._load_expected_response()

    def _load_expected_response(self):
        """Load expected responses from JSON file into memory."""
        with open(self.response_path, 'r') as f:
            self.expected_response_dict = json.load(f)

    def get_expected_response(self, result):
        """Retrieve expected response for a specific validation result.
        
        Parameters
        ----------
        result : ValidationResults
            ValidationResults object containing metadata about the function/class.
            
        Returns
        -------
        BaseModel
            Expected response validated against the ValidationClass.
        """
        expected = self.expected_response_dict[result.metadata.name]

        expected["reasoning"] = {
                "signature_parameters": [],
                "docstring_parameters": [],
                "missing_params_from_docstring": [],
                "extra_params_in_docstring": [],
                "incorrect_param_descriptions": [],
        }
        return self.ValidationClass.model_validate(expected)
    
class AssessmentComparator:
    """Compares actual LLM assessment responses against expected benchmark responses.
    
    This class provides detailed comparison logic for different types of docstring
    assessments, handling both function and class validation comparisons while
    allowing specific fields to be ignored during comparison.
    """
    
    def __init__(self, actual, expected, ignore_fields: List[str] = None):
        """Initialize comparator with actual and expected assessments.
        
        Parameters
        ----------
        actual : BaseAssessment
            The LLM-generated assessment to evaluate.
        expected : BaseAssessment
            The benchmark expected assessment to compare against.
        ignore_fields : List[str], optional
            List of field names to skip during comparison.
            Defaults to ['reasoning'] if not provided.
        """
        self.actual = actual
        self.expected = expected

        if ignore_fields is None:
            ignore_fields = ["reasoning"]

        self.ignore_fields = ignore_fields

    def compare(self):
        """Loop through each field in the actual response and expected, and compare"""
        metrics = DocstringComparison()

        for key in self.actual.model_dump():
            if key in self.ignore_fields:
                continue

            act_val = self.actual.__dict__[key]
            exp_val = self.expected.__dict__[key]

            if isinstance(act_val, ClassDocstring):
                metrics += self.compare_class_docstring(act_val, exp_val)
            elif isinstance(act_val, FunctionDocstring):
                metrics += self.compare_function_docstring(act_val, exp_val)
            else:
                metrics.field_comparison.update(key, act_val, exp_val)

        return metrics.to_mean()

    def compare_class_docstring(self, act_cd1: ClassDocstring, exp_cd2: ClassDocstring):
        """Compare class docstring assessments.
        
        Parameters
        ----------
        act_cd1 : ClassDocstring
            First class docstring assessment.
        exp_cd2 : ClassDocstring
            Second class docstring assessment to compare against.
            
        Returns
        -------
        DocstringComparison
            Comparison metrics for the class docstrings.
        """
        dac = self.compare_all_arguments(act_cd1.correct_class_arguments, exp_cd2.correct_class_arguments)
        return dac
    
    def compare_function_docstring(self, act_fd1: FunctionDocstring, exp_fd2: FunctionDocstring):
        """Compare function docstring assessments.
        
        Parameters
        ----------
        act_fd1 : FunctionDocstring
            First function docstring assessment.
        exp_fd2 : FunctionDocstring
            Second function docstring assessment to compare against.
            
        Returns
        -------
        DocstringComparison
            Comparison metrics for the function docstrings.
        """
        dac = self.compare_all_arguments(act_fd1.correct_function_arguments, exp_fd2.correct_function_arguments)

        ret_comp = ReturnValueComparison(act_fd1.correct_function_return_values, exp_fd2.correct_function_return_values)
        
        out = dac + ret_comp

        out.rets_count = len(exp_fd2.correct_function_return_values)

        return out

    def compare_all_arguments(self, act_args1: List[Argument], exp_args2: List[Argument]):
        """Compare two lists of argument specifications.
        
        Parameters
        ----------
        act_args1 : List[Argument]
            First list of arguments to compare.
        exp_args2 : List[Argument]
            Second list of arguments to compare against.
            
        Returns
        -------
        DocstringComparison
            Aggregated comparison metrics for all arguments.
        """
        docstring_comp = DocstringComparison(corrected_num_args_match=len(act_args1) == len(exp_args2))

        for a2, a1 in zip(exp_args2, act_args1):
            docstring_comp += ArgumentComparison(a1, a2)

        return docstring_comp
    
class MetricsCollector:
    """Collects, stores, and manages benchmark metrics across multiple model runs.
    
    This class handles persistence of benchmark results to CSV files, manages
    response storage, and provides functionality for generating summary statistics
    across different models and configuration styles.
    """
    
    def __init__(self, basepath = "tests/data/results/", metrics_filename='metrics.csv'):
        """Initialize metrics collector with storage configuration.
        
        Parameters
        ----------
        basepath : str, optional
            Base directory path for storing metrics and responses.
            Defaults to 'tests/data/results/'.
        metrics_filename : str, optional
            Filename for the main metrics CSV file.
            Defaults to 'metrics.csv'.
        """
        self.basepath = basepath
        self.metrics_filename = metrics_filename
        self.metrics_path = os.path.join(basepath, metrics_filename)

        if os.path.exists(self.metrics_path):
            self.metrics = pd.read_csv(self.metrics_path, index_col=False)
            self.metrics = self.metrics.set_index(['model', 'style', 'suite', 'name'])
        else:
            os.makedirs(os.path.dirname(self.metrics_path), exist_ok=True)
            self.metrics = pd.DataFrame()

    def record(self, model, style, suite, response, response_comparison: pd.DataFrame):
        """Record benchmark results for a specific model and style configuration.
        
        Parameters
        ----------
        model : str
            Name/identifier of the model being benchmarked.
        style : str
            Configuration style used (e.g., 'basic', 'reasoning', 'streamlined').
        suite : str
            Test suite being evaluated.
        response : list
            Raw response data from the model.
        response_comparison : pd.DataFrame
            DataFrame containing comparison metrics.
        """
        response_comparison['model'] = model
        response_comparison['style'] = style
        
        response_comparison = response_comparison.set_index(['model', 'style', 'suite', 'name'])

        if not self.metrics.empty:
            self.metrics = self.metrics.drop(response_comparison.index, errors='ignore')

        self.metrics = pd.concat([self.metrics, response_comparison])

        self.save_metrics()
        self.save_response(model, style, suite, response)

    def save_metrics(self):
        """Save current metrics DataFrame to CSV file."""
        self.metrics.to_csv(self.metrics_path, index=True)

    def save_response(self, model: str, style: str, suite, response: str):
        """Save raw model responses to JSON files organized by model and style.
        
        Parameters
        ----------
        model : str
            Name/identifier of the model.
        style : str
            Configuration style used.
        suite : str
            Test suites associated with the response.
        response : str
            Raw response data to save.
        """

        path_safe_model_name = self.get_path_safe_model_name(model)
        save_path = os.path.join(self.basepath, style, f'{path_safe_model_name}_{suite}_response.json')
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'w') as f:
            print("[", file=f)
            print(',\n'.join(r.to_json() for r in response), file=f)
            print("]", file=f)

    def save_summary_metrics(self):
        """Generate and save summary statistics grouped by model and style.
        
        Creates a summary CSV file with mean performance metrics across all
        test cases for each model-style combination.
        """
        filepath = os.path.join(self.basepath, f"summary_{self.metrics_filename}")

        result = (
            self
            .metrics
            .reset_index()
            .groupby(['model', 'style', 'suite'])
            .mean(numeric_only=True)
            .reset_index()
        )

        result.to_csv(filepath, index=False)

    def get_path_safe_model_name(self, model: str):
        """Converts a model name to a path format.

        Parameters
        ----------
        model : str
            The model name.

        Returns
        -------
        str
            The converted path.
        """
        punctuation = [":", "-", "."]

        translation = str.maketrans({p: "_" for p in punctuation})

        return model.translate(translation)
        

def main(): 
    """Main function to run the benchmarking process.

    This function sets up and runs the benchmarking process using a specified model.
    """
    models = [
        "gpt-5-nano-2025-08-07",
        # "gpt-5-mini-2025-08-07",
        # "claude-sonnet-4-20250514",
        "claude-3-5-haiku-20241022",
        "llama3.1:8b-instruct-q8_0",
        "phi4-mini-reasoning:3.8b",
        "phi4-mini:latest",
        "deepseek-r1:8b",
        "granite3.3:8b",
        "phi3:14b-medium-128k-instruct-q4_K_M",
        "phi4:latest",
        "gemma3:4b-it-qat",
        "qwen3:latest",
        "mistral-nemo:12b",
    ]
    styles = [
        'basic',
        # 'streamlined',
        'reasoning',
    ]

    mc = MetricsCollector()
    for model, style in itertools.product(models, styles): 
        print(f"Running benchmarks for {model} ({style})")
        benchmark(model, style, mc)

    mc.save_summary_metrics()

def benchmark(model: str, style: str, mc: MetricsCollector):
    """Benchmarks a model by comparing its output to expected responses.

    Parameters
    ----------
    model : str
        The name of the model to benchmark.
    style : str
        Configuration style to use ('basic', 'reasoning', 'streamlined').
    mc : MetricsCollector
        MetricsCollector instance for storing benchmark results.
    """
    cases = [
        TestCaseSuite(
            "function", 
            "tests/data/functions.py", 
            "tests/data/function_responses.json",
            BaseFunctionDocstringAssessment
        ),
        TestCaseSuite(
            "class", 
            "tests/data/class.py", 
            "tests/data/class_responses.json",
            BaseClassDocstringAssessment
        ),
    ]
    connection = load_model(model)

    for case in cases:
        print(f"\tRunning {case.label}...")
        metric, response = _benchmark_helper(connection, case, style)
        mc.record(model, style, case.label, response, metric)

def load_model(model):
    """Loads a model based on the provided name.

    Parameters
    ----------
    model : str
        The name of the model to load.

    Returns
    -------
    BaseConnection
        The loaded model connection.
    """
    if "claude" in model:
        return AnthropicConnection(model)
    elif 'gpt' in model:
        return OpenaiConnection(model)
    else:
        return OllamaConnection(model)

def _benchmark_helper(
    connection: BaseConnection, 
    case: TestCaseSuite,
    style: str
):
    """Run benchmark for a model against a specific test case suite.

    Parameters
    ----------
    connection : BaseConnection
        The model connection to use for validation.
    case : TestCaseSuite
        TestCaseSuite containing input files and expected responses.
    style : str
        Configuration style to use ('basic', 'reasoning', 'streamlined').

    Returns
    -------
    tuple[pd.DataFrame, list]
        Metrics DataFrame and list of validation responses.
    """
    validator = ValidationAgent(connection, AgentConfigFactory.create(style))
    parser = FileParser(case.input_path)

    runner = Runner(parser, validator)

    metrics = []
    responses = []
    for result in runner.validate_sequence():
        assessment = result.assessment
        expected = case.get_expected_response(result)

        comp_result = AssessmentComparator(assessment, expected).compare().to_dict()
        comp_result["name"] = result.metadata.name

        metrics.append(comp_result)
        responses.append(result)

    metrics = pd.DataFrame(metrics)
    metrics['suite'] = case.label

    return metrics, responses


if __name__ == "__main__":
    main()
