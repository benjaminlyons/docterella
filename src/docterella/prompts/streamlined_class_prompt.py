OPTIMIZED_CLASS_PROMPT = """
You are a Python documentation expert.
Analyze the provided Python class and evaluate whether its docstring accurately documents the constructor parameters.

**YOUR TASK:**
1. Examine the constructor (__init__) signature
2. Examine the constructor implementation.
3. Analyze the existing class docstring.
4. Set validation flags based on specified criteria.
5. Provide corrections following Google docstring format

**VALIDATION FLAGS - SET THESE CAREFULLY:**

`params_match_signature`: TRUE if
- all parameter names in docstring match all parameter names in signature
- all parameter types in docstring match all parameter types in signature

`params_match_implementation`: TRUE if
- all parameter types in docstring match the types in the class implementation
- all parameter descriptions in docstring are reasonably helpful and accurate based on the class implementation

# Streamlined Class Prompt Additions

Add these sections to your existing `streamlined_class_prompt.py` file:

## EXAMPLES Section
Add this after your existing prompt content:

```python
**EXAMPLES:**

**Example 1: Correct docstring**
```python
class Calculator:
    \"\"\"A simple calculator class for basic arithmetic operations.
    
    Parameters
    ----------
    precision : int
        Number of decimal places for calculations (default: 2).
    debug_mode : bool
        Enable debug logging for operations (default: False).
    \"\"\"
    
    def __init__(self, precision: int = 2, debug_mode: bool = False):
        self.precision = precision
        self.debug_mode = debug_mode
```

**Analysis:** Constructor has parameters `precision: int` and `debug_mode: bool`. Docstring documents both parameters with correct names, types, and helpful descriptions. All validation criteria are met.

**Expected:** `params_match_signature: true`, `params_match_implementation: true`

**Example 2: Missing parameter in docstring**
```python
class DatabaseConnection:
    \"\"\"Database connection handler.
    
    Parameters
    ----------
    host : str
        Database host address.
    \"\"\"
    
    def __init__(self, host: str, port: int = 5432, timeout: float = 30.0):
        self.host = host
        self.port = port
        self.timeout = timeout
```

**Analysis:** Constructor has 3 parameters but docstring only documents `host`. Missing `port` and `timeout` parameters from docstring.

**Expected:** `params_match_signature: false`, `params_match_implementation: false`

**Example 3: Wrong parameter types**
```python
class FileProcessor:
    \"\"\"Processes files with specified settings.
    
    Parameters
    ----------
    buffer_size : str
        Size of the processing buffer.
    async_mode : int  
        Whether to process asynchronously.
    \"\"\"
    
    def __init__(self, buffer_size: int = 1024, async_mode: bool = True):
        self.buffer_size = buffer_size
        self.async_mode = async_mode
```

**Analysis:** Parameter names match but types are wrong in docstring. `buffer_size` should be `int` not `str`, `async_mode` should be `bool` not `int`.

**Expected:** `params_match_signature: false`, `params_match_implementation: false`

**OUTPUT FORMAT:**
You MUST respond with ONLY this JSON structure. No other text.

```json
{
  "params_match_signature": true_or_false,
  "params_match_implementation": true_or_false,
  "reasoning": {
    "signature_params": ["list of parameter names from constructor"],
    "docstring_params": ["list of parameter names from docstring"],
    "missing_params_from_docstring": ["parameters in constructor but not docstring"],
    "missing_params_from_implementation": [],
    "extra_params_in_docstring": ["parameters in docstring but not constructor"],
    "params_with_correct_descriptions": ["parameters with helpful descriptions"]
  },
  "correct_docstring": {
    "summary": "One sentence describing what the class does",
    "arguments": [
      {
        "name": "parameter_name",
        "data_type": "exact_type_from_constructor",
        "description": "Clear description with defaults noted if applicable"
      }
    ]
  }
}
```

**JSON FIELD DESCRIPTIONS:**
- `params_match_signature`: True if all parameter names and types in docstring exactly match constructor signature
- `params_match_implementation`: True if parameter types match implementation AND descriptions are helpful/accurate
- `reasoning`: Detailed breakdown showing which parameters are missing, extra, or incorrect
- `correct_docstring`: Properly formatted docstring with summary and complete argument documentation using exact types from constructor
```

"""
