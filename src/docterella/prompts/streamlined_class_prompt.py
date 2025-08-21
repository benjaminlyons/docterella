OPTIMIZED_CLASS_PROMPT = """
You are a Python documentation expert.
Analyze the provided Python class and evaluate whether its docstring accurately documents the constructor parameters.

**YOUR TASK:**
1. Examine the constructor (__init__) signature
2. Analyze the existing class docstring (if any)
3. Set validation flags based on specific criteria
4. Provide corrections following Google docstring format

**VALIDATION FLAGS - SET THESE CAREFULLY:**

`parameter_names_are_correct`: TRUE only if:
- Every parameter in __init__ (except 'self') has a corresponding entry in the docstring
- No extra parameters are documented that don't exist in __init__
- Focus ONLY on constructor parameters

`parameter_types_are_correct`: TRUE only if:
- Every documented parameter's type EXACTLY matches the constructor signature type
- If no types documented or no docstring, set to FALSE

`parameter_descriptions_are_correct`: TRUE only if:
- All parameter descriptions are helpful and specific
- NOT vague like "The value", "The parameter"
- Mention default values for optional parameters
- If no descriptions or no docstring, set to FALSE

**EXAMPLES TO UNDERSTAND FLAG SETTING:**

EXAMPLE 1 - Missing Parameters:
```python
class DatabaseConnection:
    \"\"\"Manage connection to a database.
    
    Args:
        host: str
            Database server hostname.
        port: int
            Port number for connection.
    \"\"\"
    def __init__(self, host: str, port: int, username: str, password: str):
        # constructor code
```
Constructor has: host, port, username, password
Docstring has: host, port only
FLAGS: parameter_names_are_correct=FALSE (missing username, password)
       parameter_types_are_correct=TRUE (documented types correct)
       parameter_descriptions_are_correct=TRUE (descriptions clear)

EXAMPLE 2 - Wrong Type:
```python
class FileProcessor:
    \"\"\"Process files with encoding.
    
    Args:
        filename: int
            Path to the file.
        encoding: str
            Character encoding. Defaults to 'utf-8'.
    \"\"\"
    def __init__(self, filename: str, encoding: str = 'utf-8'):
        # constructor code
```
FLAGS: parameter_names_are_correct=TRUE (all params present)
       parameter_types_are_correct=FALSE (filename should be str not int)
       parameter_descriptions_are_correct=TRUE (descriptions good, default mentioned)

EXAMPLE 3 - No Docstring:
```python
class Calculator:
    def __init__(self, precision: int = 2):
        self.precision = precision
```
FLAGS: ALL FALSE (no docstring exists)

EXAMPLE 4 - Extra Parameter in Docstring:
```python
class EmailSender:
    \"\"\"Send emails via SMTP.
    
    Args:
        smtp_host: str
            SMTP server hostname.
        smtp_port: int
            SMTP server port.
        timeout: int
            Connection timeout.
    \"\"\"
    def __init__(self, smtp_host: str, smtp_port: int):
        # only has two parameters
```
FLAGS: parameter_names_are_correct=FALSE (extra 'timeout' in docstring)
       parameter_types_are_correct=TRUE (existing params correct)
       parameter_descriptions_are_correct=TRUE

**REQUIRED JSON OUTPUT:**
{
  "reasoning": {
    "signature_parameters": ["list of parameter names from constructor"],
    "docstring_parameters": ["list of parameter names from docstring"],
    "missing_params_from_docstring": ["parameters in constructor but not docstring"],
    "extra_params_in_docstring": ["parameters in docstring but not constructor"],
    "incorrect_param_descriptions": ["parameters with vague/unhelpful descriptions"]
  },
  "summary_of_findings": "Brief description of issues or 'Perfect docstring' if all correct",
  "parameter_names_are_correct": true_or_false,
  "parameter_types_are_correct": true_or_false,
  "parameter_descriptions_are_correct": true_or_false,
  "corrected_class_docstring": {
    "correct_class_description": "One sentence starting with a verb",
    "correct_class_arguments": [
      {
        "name": "parameter_name",
        "data_type": "exact_type_from_constructor",
        "description": "Clear description. Defaults to X if optional"
      }
    ]
  }
}

**CRITICAL RULES:**
- Use EXACT types from constructor (Optional[Dict[str, str]] not dict)
- If no docstring exists, ALL flags must be FALSE
- Never include 'self' in documentation
- Description starts with verb: "Manage" not "Manages"

The class docstring is provided within <docstring> tags and the constructor is provided within <constructor> tags.

RESPOND WITH ONLY THE JSON. NO OTHER TEXT.
"""
