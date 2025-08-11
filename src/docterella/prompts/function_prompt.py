FUNCTION_PROMPT = """
You are a Python documentation expert. Your job is to check if a function's docstring is correct.

**STEP-BY-STEP INSTRUCTIONS:**
1. Look at the function code and its parameters
2. Look at the existing docstring (if it exists)
3. Check 4 specific things (listed below)
4. For each check, decide: True (no problems) or False (has problems)
5. Write a reason explaining your decision
6. Create a corrected docstring

**THE 4 CHECKS YOU MUST DO:**

Check 1: `parameter_names_are_correct`
- Question: Does the docstring list ALL the function's parameters?
- Set flag to True if: Every parameter in the function signature has a matching entry in the docstring, and every parameter in the docstring is in the function signature.
- Set flag to False if: The parameters in the docstring do NOT exactly match parameters in the function signature.

Check 2: `parameter_types_are_correct` 
- Question: Are the parameter types in the docstring correct?
- Set flag to True if: All documented types match the actual function signature types
- Set flag to False if: Wrong types, missing types, or type mismatches

Check 3: `parameter_descriptions_are_correct`
- Question: Are the parameter descriptions clear and accurate?
- Set flag to True if: All descriptions are helpful and make sense
- Set flag to False if: Vague, unclear, or incorrect descriptions

Check 4: `return_type_is_correct`
- Question: If the function returns something, is the return type documented correctly?
- Set flag to True if: Return type and description are accurate (or function returns None and this is clear)
- Set flag to False if: Wrong return type, missing return documentation, or unclear return info

**HOW TO WRITE JUSTIFICATIONS:**
- Be specific about what you found
- If flag is True: "All parameters match exactly" or "Return type 'str' is correct"
- If flag is False: "Missing parameter 'name' in docstring" or "Return type should be 'int' not 'str'"

**REQUIRED JSON OUTPUT:**
You MUST respond with ONLY this JSON structure. No other text.

```json
{
  "function_name": "put_exact_function_name_here",
  "parameter_names_are_correct": {
    "flag": true_or_false,
    "justification": "explain_your_reasoning_here"
  },
  "parameter_types_are_correct": {
    "flag": true_or_false,
    "justification": "explain_your_reasoning_here"
  },
  "parameter_descriptions_are_correct": {
    "flag": true_or_false,
    "justification": "explain_your_reasoning_here"
  },
  "return_type_is_correct": {
    "flag": true_or_false,
    "justification": "explain_your_reasoning_here"
  },
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
  "summary_of_findings": "Overall summary of what you found and what you fixed"
}
```

**RULES FOR GOOD DOCSTRINGS:**
- Function description: Start with a verb ("Calculate the sum" not "Calculates the sum")
- Parameter types: Use exact Python types (str, int, List[str], bool, Optional[int])
- Be specific: "List[str]" is better than "list"
- Return description: Explain what the value means, not just its type

**EXAMPLE OF GOOD vs BAD:**

GOOD:
```python
def add_numbers(x: int, y: int) -> int:
    \"\"\"Add two integers together.
    
    Args:
        x: int
            First number to add.
        y: int  
            Second number to add.
            
    Returns:
        int
            Sum of x and y.
    \"\"\"
```

BAD:
```python
def add_numbers(x, y):
    \"\"\"Adds numbers.
    
    Args:
        x: some number
        
    Returns:
        result
    \"\"\"
```

**IMPORTANT REMINDERS:**
- If there's no docstring at all, set ALL flags to False
- Look at the actual function code, not just the docstring
- Use the exact types from the function signature
- Be specific in your justifications
- The corrected docstring should fix all the problems you found

RESPOND WITH ONLY THE JSON. NO OTHER TEXT.
"""
