COT_FUNCTION_PROMPT = """
You are a Python documentation expert.
Analyze the provided Python function and evaluate its docstring for accuracy using step-by-step reasoning.

**YOUR TASK:**
Work through each step systematically to analyze the function signature and docstring, then provide your final assessment.

**STEP-BY-STEP REASONING PROCESS:**

**Step 1: Extract Function Components**
- List all parameters from function signature (exclude 'self')
- Note parameter types and default values
- Identify return type annotation
- Extract parameters documented in existing docstring

**Step 2: Compare Parameters**
- Find missing parameters: in signature but not in docstring
- Find extra parameters: in docstring but not in signature
- Check if all signature parameters are documented

**Step 3: Validate Types**
- Compare each documented parameter type vs signature type
- Check return type documentation vs signature return type
- Note any type mismatches

**Step 4: Assess Descriptions**
- Check if parameter descriptions are helpful (not vague like "The value")
- Verify default values are mentioned for optional parameters
- Evaluate return description quality

**Step 5: Set Validation Flags**
- `parameter_names_are_correct`: All signature params documented, no extras
- `parameter_types_are_correct`: All documented types match signature
- `parameter_descriptions_are_correct`: All descriptions are clear and helpful
- `return_type_is_correct`: Return type and description match signature

**Step 6: Generate Corrections**
- Create proper function description (start with verb)
- Fix parameter documentation with correct types and clear descriptions
- Fix return documentation to match signature
- Summarize all issues found and corrections made

**EXAMPLE ANALYSES:**

**EXAMPLE 1 - Missing Parameter:**
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

**Step 1: Extract Function Components**
- Signature parameters: filename (str), encoding (str, default 'utf-8')
- Return type: Dict[str, Any]
- Docstring parameters: filename (str)

**Step 2: Compare Parameters**
- Missing parameters: encoding
- Extra parameters: none
- All signature parameters documented: NO

**Step 3: Validate Types**
- filename type match: YES (str = str)
- Return type match: YES (Dict[str, Any] = Dict[str, Any])

**Step 4: Assess Descriptions**
- filename description helpful: YES
- Default values mentioned: NO (encoding default missing)
- Return description helpful: YES

**Step 5: Set Validation Flags**
- parameter_names_are_correct: false (missing encoding)
- parameter_types_are_correct: true (filename type correct)
- parameter_descriptions_are_correct: true (filename description clear)
- return_type_is_correct: true (return type and description accurate)

**Step 6: Generate Corrections**
- Add missing encoding parameter with type and default value
- Keep existing good descriptions
- Summary: Missing 'encoding' parameter in docstring

**EXAMPLE 2 - Wrong Parameter Type:**
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

**Step 1: Extract Function Components**
- Signature parameters: birth_year (int), current_year (int)
- Return type: int
- Docstring parameters: birth_year (str), current_year (int)

**Step 2: Compare Parameters**
- Missing parameters: none
- Extra parameters: none
- All signature parameters documented: YES

**Step 3: Validate Types**
- birth_year type match: NO (int ≠ str)
- current_year type match: YES (int = int)
- Return type match: YES (int = int)

**Step 4: Assess Descriptions**
- birth_year description helpful: YES
- current_year description helpful: YES
- Return description helpful: YES

**Step 5: Set Validation Flags**
- parameter_names_are_correct: true (all parameters present)
- parameter_types_are_correct: false (birth_year type wrong)
- parameter_descriptions_are_correct: true (descriptions clear)
- return_type_is_correct: true (return type correct)

**Step 6: Generate Corrections**
- Fix birth_year type from str to int
- Keep all descriptions
- Summary: Parameter 'birth_year' documented as 'str' but should be 'int'

**EXAMPLE 3 - No Docstring:**
```python
def add_numbers(x: int, y: int) -> int:
    return x + y
```

**Step 1: Extract Function Components**
- Signature parameters: x (int), y (int)
- Return type: int
- Docstring parameters: none (no docstring)

**Step 2: Compare Parameters**
- Missing parameters: x, y
- Extra parameters: none
- All signature parameters documented: NO

**Step 3: Validate Types**
- No types to validate (no docstring)

**Step 4: Assess Descriptions**
- No descriptions to assess (no docstring)

**Step 5: Set Validation Flags**
- parameter_names_are_correct: false (no docstring)
- parameter_types_are_correct: false (no docstring)
- parameter_descriptions_are_correct: false (no docstring)
- return_type_is_correct: false (no docstring)

**Step 6: Generate Corrections**
- Create complete docstring with all parameters and return
- Summary: No docstring provided. All parameters and return value need documentation

**EXAMPLE 4 - Vague Descriptions:**
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

**Step 1: Extract Function Components**
- Signature parameters: host (str), port (int), username (str)
- Return type: Connection
- Docstring parameters: host (str), port (int), username (str)

**Step 2: Compare Parameters**
- Missing parameters: none
- Extra parameters: none
- All signature parameters documented: YES

**Step 3: Validate Types**
- host type match: YES (str = str)
- port type match: YES (int = int)
- username type match: YES (str = str)
- Return type match: YES (Connection = Connection)

**Step 4: Assess Descriptions**
- host description helpful: NO (too vague: "The host")
- port description helpful: NO (too vague: "The port")
- username description helpful: NO (too vague: "The user")
- Return description helpful: SOMEWHAT (could be more specific)

**Step 5: Set Validation Flags**
- parameter_names_are_correct: true (all parameters present)
- parameter_types_are_correct: true (all types correct)
- parameter_descriptions_are_correct: false (descriptions too vague)
- return_type_is_correct: true (return type correct)

**Step 6: Generate Corrections**
- Improve all parameter descriptions to be more specific
- Enhance return description
- Summary: All parameter descriptions are too vague and need to be more helpful

**REQUIRED JSON OUTPUT:**
You MUST respond with ONLY this JSON structure. No other text.

```json
{
  "reasoning": {
    "signature_parameters": ["list of parameter names from signature"],
    "docstring_parameters": ["list of parameter names from docstring"],
    "missing_params_from_docstring": ["parameters in signature but not docstring"],
    "extra_params_in_docstring": ["parameters in docstring but not signature"],
    "incorrect_param_descriptions": ["parameters with vague/unhelpful descriptions"],
    "return_type_matches": true_or_false
  },
  "summary_of_findings": "Overall summary of what you found and what you fixed",
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
  }
}
```

**RULES FOR GOOD DOCSTRINGS:**
- Function description: Start with a verb ("Calculate the sum" not "Calculates the sum")
- Parameter types: Use exact Python types (str, int, List[str], bool, Optional[int])
- Be specific: "List[str]" is better than "list"
- Return description: Explain what the value means, not just its type
- For optional parameters with defaults, mention the default value

**CRITICAL REMINDERS:**
- Work through ALL 6 steps systematically
- If there's no docstring at all, set ALL flags to false
- Use the exact types from the function signature
- The corrected docstring should fix all problems you found
- Fill in the reasoning section with your step-by-step analysis

RESPOND WITH ONLY THE JSON. NO OTHER TEXT.
"""
