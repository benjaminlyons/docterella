"""
Test file containing Python functions with various docstring issues
for testing the docterella package validation functionality.
"""

from typing import List, Optional, Dict, Union
import json


def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle.
    
    Args:
        length: float
            Length of the rectangle in units.
        width: float
            Width of the rectangle in units.
            
    Returns:
        float
            Area of the rectangle in square units.
    """
    return length * width


def create_user_profile(name: str, age: int, city: str) -> str:
    """Create a user profile string.
    
    Args:
        name: str
            Full name of the user.
        age: int
            Age of the user in years.
            
    Returns:
        str
            Formatted user profile string.
    """
    return f"{name}, {age} years old, lives in {city}"


def count_item_frequencies(items: List[str], count: int) -> Dict[str, int]:
    """Count occurrences of items.
    
    Args:
        items: str
            Items to count.
        count: str
            Maximum count limit.
            
    Returns:
        list
            Dictionary of item counts.
    """
    result = {}
    for item in items[:count]:
        result[item] = result.get(item, 0) + 1
    return result


def add_integers(x: int, y: int) -> int:
    """Add two numbers together.
    
    Args:
        x: int
            First number to add.
        y: int
            Second number to add.
        z: int
            Third number to add.
        multiplier: float
            Factor to multiply the result.
            
    Returns:
        int
            Sum of the numbers.
    """
    return x + y


def validate_dataset(data: List[Dict[str, Union[str, int]]], threshold: float) -> bool:
    """Process data.
    
    Args:
        data: List[Dict[str, Union[str, int]]]
            Some data.
        threshold: float
            A number.
            
    Returns:
        bool
            True or False.
    """
    if not data:
        return False
    return len(data) > threshold


def load_config_file(file_path: str, encoding: str = "utf-8") -> Dict[str, any]:
    """Load configuration from a JSON file.
    
    Args:
        file_path: str
            Path to the JSON configuration file.
        encoding: str
            File encoding to use when reading.
    """
    with open(file_path, 'r', encoding=encoding) as f:
        return json.load(f)


def calculate_mean(numbers: List[int]) -> float:
    """Calculate the average of a list of numbers.
    
    Args:
        numbers: List[int]
            List of integers to average.
            
    Returns:
        int
            Average value of the numbers.
    """
    return sum(numbers) / len(numbers)


def normalize_string(value: str, case_sensitive: bool = False):
    if case_sensitive:
        return value
    return value.lower()


def get_system_status():
    """This function does something mysterious.
    
    It performs operations but nobody knows what parameters it takes
    or what it returns.
    """
    return "mystery solved"


def format_text_output(text: str, max_length: int, pad_char: str = " ") -> str:
    """Format text string.
    
    Args:
        content: str
            The text content to format.
        max_length: float
            Maximum length allowed.
        
    Returns:
        list
            The formatted text.
    """
    if len(text) > max_length:
        return text[:max_length]
    return text.ljust(max_length, pad_char)


def build_config_string(name: str, config: Optional[Dict[str, str]] = None) -> str:
    """Generate configuration string.
    
    Args:
        name: str
            Name for the configuration.
        config: Dict[str, str]
            Configuration dictionary with string values.
            
    Returns:
        str
            Formatted configuration string.
    """
    if config is None:
        config = {}
    return f"{name}: {config}"


def print_to_console(message: str) -> None:
    """Print a message to the console.
    
    Args:
        message: str
            Message to print to the console.
            
    Returns:
        None
            This function does not return a value.
    """
    print(message)

