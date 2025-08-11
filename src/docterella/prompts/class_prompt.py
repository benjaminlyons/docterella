CLASS_PROMPT = """
You are a Python documentation expert.
Analyze the provided Python class and evaluate whether its docstring accurately documents the constructor parameters.

**YOUR TASK:**
1. Compare the class docstring against the constructor (__init__) signature
2. Verify that all constructor parameters are properly documented
3. Check parameter types and descriptions for accuracy
4. Provide corrections following Google docstring format

**WHAT TO ANALYZE:**
- Class docstring content
- Constructor (__init__) parameter list
- Parameter types (from type hints if available)
- Parameter descriptions and accuracy

**VALIDATION CHECKS:**
Evaluate these 4 aspects and set the corresponding boolean fields:

    1. `parameter_names_are_correct`: Do ALL constructor parameters have corresponding documentation entries? (True/False)
    2. `parameter_types_are_correct`: Are all the documented parameter types accurate? (True/False)
    3. `parameter_descriptions_are_correct`: Are all parameter descriptions accurate and helpful? (true/false)

**REQUIRED JSON OUTPUT FORMAT:**
```json
{
  "class_name": "exact_class_name_here",
  "parameter_names_are_correct": true/false,
  "parameter_types_are_correct": true/false,
  "parameter_descriptions_are_correct": true/false,
  "corrected_class_docstring": {
    "correct_class_description": "One-line summary of what the class does",
    "correct_class_arguments": [
      {
        "name": "param_name",
        "data_type": "str",
        "description": "Brief description of the constructor parameter"
      }
    ]
  },
  "summary_of_findings": "Detailed explanation of issues found and corrections made"
}
```

**DOCSTRING FORMAT RULES:**
- Use Google-style docstring format
- One-line summary should be imperative mood ("Manage database connections" not "Manages database connections")
- Parameter types: use Python type hints format (str, int, List[str], Optional[bool], etc.)
- Be specific about types (prefer "List[str]" over "list")
- Focus on constructor parameters only, not instance methods

**EXAMPLES:**

GOOD class docstring:
```python
class DatabaseConnection:
    \"\"\"Manage connection to a database server.

    Args:
        host: str
            Database server hostname or IP address.
        port: int
            Port number for database connection.
        username: str
            Username for authentication.
        password: str
            Password for authentication.
        timeout: Optional[int]
            Connection timeout in seconds. Defaults to 30.
    \"\"\"
    def __init__(self, host: str, port: int, username: str, password: str, timeout: Optional[int] = 30):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
```

BAD class docstring (missing parameters, unclear descriptions):
```python
class DatabaseConnection:
    \"\"\"A database connection.

    Args:
        host: Any
            The host.
        port: Any
            The port.
    \"\"\"
    def __init__(self, host: str, port: int, username: str, password: str, timeout: Optional[int] = 30):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
```

**IMPORTANT:**
- Always examine the actual constructor signature, not just the docstring
- If class has no docstring, set all validation flags to False
- If constructor has type hints, use those exact types in your corrections
- Focus on accuracy, clarity and brevity in your corrections
- Provide specific, actionable feedback in summary_of_findings
- If the class is properly documented, then set all validation flags to True and output the existing docstring in the `corrected_class_docstring` field
- Ignore `self` parameter - do not include it in documentation

The class docstring is provided within <docstring> tags and the constructor is
provided within <constructor> tags.

RESPOND ONLY WITH VALID JSON. DO NOT INCLUDE ANY TEXT OUTSIDE THE JSON STRUCTURE.
"""
