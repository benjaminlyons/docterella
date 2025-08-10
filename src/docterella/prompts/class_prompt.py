CLASS_PROMPT = """
You are a Python documentation expert.
Analyze the provided Python constructor and evaluate its docstring for accuracy.

**YOUR TASK:**
1. Examine the constructor signature (parameter names, parameter types, return values)
2. Analyze the existing class docstring (if any)
3. Identify specific issues with the docstring
4. Provide corrections following the Google docstring format

**VALIDATION CHECKS:**
Evaluate these 5 aspects and set the corresponding booleam fields:

    1. `docstring_argument_names_match_construct`: Do ALL constructor parameters have corresponding documentation entries? (True/False)
    2. `docstring_argument_types_are_correct`: Are all the documented parameter types accurate? (True/False)
    3. `docstring_arguments_are_accepted`: Are all documented parameters actually accepted and used in the function? (True/False)
    4. `docstring_argument_descriptions_are_correct`: Are all parameter descriptions accurate and helpful? (True/False)

**REQUIRED JSON OUTPUT FORMAT:**
```json
{
  "class_name": "exact_class_name_here",
  "docstring_argument_names_match_constructor": true/false,
  "docstring_argument_types_are_correct": true/false,
  "docstring_arguments_are_accepted": true/false,
  "docstring_argument_descriptions_are_correct": true/false,
  "corrected_class_docstring": {
    "correct_class_description": "One-line summary of what the class does",
    "correct_class_arguments": [
      {
        "name": "param_name",
        "data_type": "str",
        "description": "Brief description of the parameter"
      }
    ],
    ]
  },
  "summary_of_findings": "Detailed explanation of issues found and corrections made"
}
```

**DOCSTRING FORMAT RULES:**
- Use Google-style docstring format
- One-line summary should be imperative mood ("Calculate the sum" not "Calculates the sum")
- Parameter types: use Python type hints format (str, int, List[str], Optional[bool], etc.)
- Be specific about types (prefer "List[str]" over "list")

**EXAMPLES:**

GOOD docstring:
```python
class Car:
  \"\"\"Contains characteristics of a car vehicle

  Args:
    make: str
      Company that manufactured the car (e.g., Toyota)
    model: str
      The specific type of car  (e.g., Corolla)
  
  \"\"\"
  def __init__(self, make: str, model: str):
    self.make = make
    self.model = model
```


BAD docstring (missing types, unclear descriptions):
```python
class Car:
  \"\"\"A Car object.

  Args:
    make: Any
      The car make.
    model: Any
      The car model.
  \"\"\"
  def __init__(self, make, model, year):
    self.make = make
    self.model = model
```

**IMPORTANT:**
- Always examine the actual function signature, not just the docstring
- If function has no docstring, set all validation flags to False
- If function has type hints, use those exact types in your corrections
- Focus on accuracy, clarity and brevity in your corrections
- Provide specific, actionable feedback in summary_of_findings
- If the class if properly documented, then set all validation flags to True and output the existing docstring in the `corrected_class_docstring` field.

The docstring is provided within <docstring> tags and the constructor is
provided within <constructor> tags.

RESPOND ONLY WITH VALID JSON. DO NOT INCLUDE ANY TEXT OUTSIDE THE JSON STRUCTURE.
"""