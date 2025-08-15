FUNCTION_PROMPT = """
You are a Python documentation expert.
Analyze the provided Python function and evaluate its docstring for accuracy.

**YOUR TASK:**
1. Examine the function signature (parameter names, parameter types, return values)
2. Analyze the existing docstring (if any)
3. Identify specific issues with the docstring
4. Provide corrections following the Google docstring format

**VALIDATION CHECKS:**
Evaluate these 4 aspects and set the corresponding booleam fields:

1. `parameter_names_are_correct`: Do ALL function parameters have corresponding documentation entries? (true/false)
2. `parameter_types_are_correct`: Are all the documented parameter types accurate? (true/false)
4. `parameter_descriptions_are_correct`: Are all parameter descriptions accurate and helpful? (true/false)
5. `return_type_is_correct`: If function returns a value, is the return type correctly documented? (true/false)

**EXAMPLE ANALYSES:**

**EXAMPLE 1 - Function with missing parameter:**
```python
def process_data(filename: str, encoding: str = 'utf-8') -> Dict[str, Any]:
    \"\"\"Process data from a file.
    
    Args:
        filename: str
            Path to the file to process.
            
    Returns:
        Dict[str, Any]
            Processed data as dictionary.
    \"\"\"
```

Step 1 - Extract parameters from signature:
- filename: str (required)
- encoding: str (optional, default 'utf-8')

Analysis:
- parameter_names_are_correct: false (missing 'encoding' parameter in docstring)
- parameter_types_are_correct: true (filename type is correct)
- parameter_descriptions_are_correct: true (filename description is clear)
- return_type_is_correct: true (return type and description are accurate)

**EXAMPLE 2 - Function with wrong parameter type:**
```python
def calculate_age(birth_year: int, current_year: int) -> int:
    \"\"\"Calculate person's age.
    
    Args:
        birth_year: str
            Year the person was born.
        current_year: int
            Current year.
            
    Returns:
        int
            Age in years.
    \"\"\"
```

Step 1 - Extract parameters from signature:
- birth_year: int (required)
- current_year: int (required)

Analysis:
- parameter_names_are_correct: true (all parameters present)
- parameter_types_are_correct: false (birth_year should be 'int' not 'str')
- parameter_descriptions_are_correct: true (descriptions are clear)
- return_type_is_correct: true (return type is correct)

**EXAMPLE 3 - Function with no docstring:**
```python
def add_numbers(x: int, y: int) -> int:
    return x + y
```

Step 1 - Extract parameters from signature:
- x: int (required)
- y: int (required)

Analysis:
- parameter_names_are_correct: false (no docstring at all)
- parameter_types_are_correct: false (no docstring at all)
- parameter_descriptions_are_correct: false (no docstring at all)
- return_type_is_correct: false (no docstring at all)

**EXAMPLE 4 - Function with extra parameter in docstring:**
```python
def format_name(first: str, last: str) -> str:
    \"\"\"Format a person's full name.
    
    Args:
        first: str
            First name.
        middle: str
            Middle name.
        last: str
            Last name.
            
    Returns:
        str
            Formatted full name.
    \"\"\"
```

Step 1 - Extract parameters from signature:
- first: str (required)
- last: str (required)

Analysis:
- parameter_names_are_correct: false (docstring includes 'middle' parameter that doesn't exist in function)
- parameter_types_are_correct: true (existing parameters have correct types)
- parameter_descriptions_are_correct: true (descriptions are clear)
- return_type_is_correct: true (return type is correct)

**EXAMPLE 5 - Function with vague descriptions:**
```python
def connect_database(host: str, port: int, username: str) -> Connection:
    \"\"\"Connect to database.
    
    Args:
        host: str
            The host.
        port: int
            The port.
        username: str
            The user.
            
    Returns:
        Connection
            Connection object.
    \"\"\"
```

Step 1 - Extract parameters from signature:
- host: str (required)
- port: int (required)
- username: str (required)

Analysis:
- parameter_names_are_correct: true (all parameters present)
- parameter_types_are_correct: true (all types are correct)
- parameter_descriptions_are_correct: false (descriptions are too vague - "The host", "The port", "The user")
- return_type_is_correct: true (return type is correct but could be more descriptive)

**EXAMPLE 6 - Function with missing return documentation:**
```python
def validate_email(email: str) -> bool:
    \"\"\"Validate an email address.
    
    Args:
        email: str
            Email address to validate.
    \"\"\"
```

Step 1 - Extract parameters from signature:
- email: str (required)

Analysis:
- parameter_names_are_correct: true (all parameters present)
- parameter_types_are_correct: true (email type is correct)
- parameter_descriptions_are_correct: true (description is clear)
- return_type_is_correct: false (missing return documentation entirely)

**EXAMPLE 7 - Function with complex types and defaults:**
```python
def process_items(items: List[Dict[str, Any]], max_count: int = 100, filters: Optional[Set[str]] = None) -> Tuple[List[str], int]:
    \"\"\"Process a list of item dictionaries.
    
    Args:
        items: List[Dict[str, Any]]
            List of item dictionaries to process.
        max_count: int
            Maximum number of items to process. Defaults to 100.
        filters: Optional[Set[str]]
            Set of filter strings to apply. Defaults to None.
            
    Returns:
        Tuple[List[str], int]
            Tuple containing list of processed item names and count of items processed.
    \"\"\"
```

Step 1 - Extract parameters from signature:
- items: List[Dict[str, Any]] (required)
- max_count: int (optional, default 100)
- filters: Optional[Set[str]] (optional, default None)

Analysis:
- parameter_names_are_correct: true (all parameters present and exact match)
- parameter_types_are_correct: true (all complex types match exactly)
- parameter_descriptions_are_correct: true (all descriptions are clear and mention defaults)
- return_type_is_correct: true (complex return type documented correctly)

**EXAMPLE 8 - Perfect docstring:**
```python
def send_email(recipient: str, subject: str, body: str, attachments: Optional[List[str]] = None) -> bool:
    \"\"\"Send an email to a recipient.
    
    Args:
        recipient: str
            Email address of the recipient.
        subject: str
            Subject line of the email.
        body: str
            Body content of the email.
        attachments: Optional[List[str]]
            List of file paths to attach. Defaults to None.
            
    Returns:
        bool
            true if email was sent successfully, false otherwise.
    \"\"\"
```

Step 1 - Extract parameters from signature:
- recipient: str (required)
- subject: str (required)
- body: str (required)
- attachments: Optional[List[str]] (optional, default None)

Analysis:
- parameter_names_are_correct: true (all parameters present and exact match)
- parameter_types_are_correct: true (all types match exactly)
- parameter_descriptions_are_correct: true (all descriptions are clear and helpful)
- return_type_is_correct: true (return type and description are accurate)

**REQUIRED JSON OUTPUT:**
You MUST respond with ONLY this JSON structure. No other text.

```json
{
  "summary_of_findings": "Overall summary of what you found and what you fixed"
  "parameter_names_are_correct": true_or_false,
  "parameter_types_are_correct": true_or_false,
  "parameter_descriptions_are_correct": true_or_false,
  "return_type_is_correct": true_or_false,
  "corrected_function_docstring": {
    "correct_function_description": "One sentence describing what the function does",
    "correct_function_arguments": [
      {
        "name": "parameter_name",
        "data_type": "parameter_type",
        "description": "what_this_parameter_does"
      }
    ],
    "correct_function_return_values": [
      {
        "data_type": "return_type",
        "description": "what_gets_returned"
      }
    ]
  },
}
```


**RULES FOR GOOD DOCSTRINGS:**
- Function description: Start with a verb ("Calculate the sum" not "Calculates the sum")
- Parameter types: Use exact Python types (str, int, List[str], bool, Optional[int])
- Be specific: "List[str]" is better than "list"
- Return description: Explain what the value means, not just its type
- For optional parameters with defaults, mention the default value

**CRITICAL REMINDERS:**
- If there's no docstring at all, set ALL flags to false
- Look at the actual function code, not just the docstring
- Use the exact types from the function signature
- Be specific in your justifications
- The corrected docstring should fix all the problems you found

**PARAMETER EXTRACTION CHECKLIST:**
- I have identified all parameters in the function signature
= I have noted their types (if provided)
- I have noted any default values
- I have excluded 'self' from instance methods
- I have not invented any parameters

RESPOND WITH ONLY THE JSON. NO OTHER TEXT.
"""
