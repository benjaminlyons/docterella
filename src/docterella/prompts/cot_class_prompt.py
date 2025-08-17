COT_CLASS_PROMPT = """
You are a Python documentation expert.
Analyze the provided Python class and evaluate its docstring for accuracy using step-by-step reasoning.

**YOUR TASK:**
Work through each step systematically to analyze the constructor signature and class docstring, then provide your final assessment.

**STEP-BY-STEP REASONING PROCESS:**

**Step 1: Extract Constructor Components**
- List all parameters from constructor signature (exclude 'self')
- Note parameter types and default values
- Extract parameters documented in existing class docstring

**Step 2: Compare Parameters**
- Find missing parameters: in constructor but not in docstring
- Find extra parameters: in docstring but not in constructor
- Check if all constructor parameters are documented

**Step 3: Validate Types**
- Compare each documented parameter type vs constructor type
- Note any type mismatches

**Step 4: Assess Descriptions**
- Check if parameter descriptions are helpful (not vague like "The value")
- Verify default values are mentioned for optional parameters
- Evaluate description quality and specificity

**Step 5: Set Validation Flags**
- `parameter_names_are_correct`: All constructor params documented, no extras
- `parameter_types_are_correct`: All documented types match constructor
- `parameter_descriptions_are_correct`: All descriptions are clear and helpful

**Step 6: Generate Corrections**
- Create proper class description (start with verb)
- Fix parameter documentation with correct types and clear descriptions
- Summarize all issues found and corrections made

**EXAMPLE ANALYSES:**

**EXAMPLE 1 - Missing Parameter:**
```python
class DatabaseClient:
    \"\"\"Manage connections to database servers.

    Args:
        host: str
            Database server hostname.
        port: int
            Port number for connection.
    \"\"\"
    def __init__(self, host: str, port: int, username: str, ssl_enabled: bool = False):
        self.host = host
        self.port = port
        self.username = username
        self.ssl_enabled = ssl_enabled
```

**Step 1: Extract Constructor Components**
- Constructor parameters: host (str), port (int), username (str), ssl_enabled (bool, default False)
- Docstring parameters: host (str), port (int)

**Step 2: Compare Parameters**
- Missing parameters: username, ssl_enabled
- Extra parameters: none
- All constructor parameters documented: NO

**Step 3: Validate Types**
- host type match: YES (str = str)
- port type match: YES (int = int)

**Step 4: Assess Descriptions**
- host description helpful: YES
- port description helpful: YES
- Default values mentioned: NO (ssl_enabled default missing)

**Step 5: Set Validation Flags**
- parameter_names_are_correct: false (missing username, ssl_enabled)
- parameter_types_are_correct: true (documented types correct)
- parameter_descriptions_are_correct: true (existing descriptions clear)

**Step 6: Generate Corrections**
- Add missing username and ssl_enabled parameters
- Include default value for ssl_enabled
- Summary: Missing 'username' and 'ssl_enabled' parameters in docstring

**EXAMPLE 2 - Wrong Parameter Type:**
```python
class AudioPlayer:
    \"\"\"Play audio files with volume control.

    Args:
        file_path: int
            Path to the audio file.
        volume: str
            Playback volume level.
        auto_play: str
            Start playing immediately.
    \"\"\"
    def __init__(self, file_path: str, volume: float = 0.8):
        self.file_path = file_path
        self.volume = volume
```

**Step 1: Extract Constructor Components**
- Constructor parameters: file_path (str), volume (float, default 0.8)
- Docstring parameters: file_path (int), volume (str), auto_play (str)

**Step 2: Compare Parameters**
- Missing parameters: none from constructor
- Extra parameters: auto_play
- All constructor parameters documented: NO (extra param exists)

**Step 3: Validate Types**
- file_path type match: NO (str ≠ int)
- volume type match: NO (float ≠ str)

**Step 4: Assess Descriptions**
- file_path description helpful: YES
- volume description helpful: YES
- Default values mentioned: NO (volume default missing)

**Step 5: Set Validation Flags**
- parameter_names_are_correct: false (extra auto_play parameter)
- parameter_types_are_correct: false (file_path and volume types wrong)
- parameter_descriptions_are_correct: true (descriptions clear)

**Step 6: Generate Corrections**
- Fix file_path type from int to str
- Fix volume type from str to float
- Remove auto_play parameter
- Add default value for volume
- Summary: Type mismatches and extra parameter in docstring

**EXAMPLE 3 - No Docstring:**
```python
class CacheManager:
    def __init__(self, cache_size: int = 1024, expiry_seconds: int = 3600, 
                 persistent: bool = True, compression: Optional[str] = None):
        self.cache_size = cache_size
        self.expiry_seconds = expiry_seconds
        self.persistent = persistent
        self.compression = compression
```

**Step 1: Extract Constructor Components**
- Constructor parameters: cache_size (int, default 1024), expiry_seconds (int, default 3600), persistent (bool, default True), compression (Optional[str], default None)
- Docstring parameters: none (no docstring)

**Step 2: Compare Parameters**
- Missing parameters: cache_size, expiry_seconds, persistent, compression
- Extra parameters: none
- All constructor parameters documented: NO

**Step 3: Validate Types**
- No types to validate (no docstring)

**Step 4: Assess Descriptions**
- No descriptions to assess (no docstring)

**Step 5: Set Validation Flags**
- parameter_names_are_correct: false (no docstring)
- parameter_types_are_correct: false (no docstring)
- parameter_descriptions_are_correct: false (no docstring)

**Step 6: Generate Corrections**
- Create complete class docstring with all parameters
- Include all default values
- Summary: No docstring provided. All parameters need documentation

**EXAMPLE 4 - Vague Descriptions:**
```python
class FileUploader:
    \"\"\"Upload files to remote storage.

    Args:
        endpoint: str
            The endpoint.
        chunk_size: int
            The size.
        verify_ssl: bool
            The verification.
        headers: dict
            The headers.
    \"\"\"
    def __init__(self, endpoint: str, chunk_size: int = 8192, verify_ssl: bool = True, 
                 headers: Optional[Dict[str, str]] = None):
        self.endpoint = endpoint
        self.chunk_size = chunk_size
        self.verify_ssl = verify_ssl
        self.headers = headers
```

**Step 1: Extract Constructor Components**
- Constructor parameters: endpoint (str), chunk_size (int, default 8192), verify_ssl (bool, default True), headers (Optional[Dict[str, str]], default None)
- Docstring parameters: endpoint (str), chunk_size (int), verify_ssl (bool), headers (dict)

**Step 2: Compare Parameters**
- Missing parameters: none
- Extra parameters: none
- All constructor parameters documented: YES

**Step 3: Validate Types**
- endpoint type match: YES (str = str)
- chunk_size type match: YES (int = int)
- verify_ssl type match: YES (bool = bool)
- headers type match: NO (Optional[Dict[str, str]] ≠ dict)

**Step 4: Assess Descriptions**
- endpoint description helpful: NO (too vague: "The endpoint")
- chunk_size description helpful: NO (too vague: "The size")
- verify_ssl description helpful: NO (too vague: "The verification")
- headers description helpful: NO (too vague: "The headers")
- Default values mentioned: NO (missing all defaults)

**Step 5: Set Validation Flags**
- parameter_names_are_correct: true (all parameters present)
- parameter_types_are_correct: false (headers type wrong)
- parameter_descriptions_are_correct: false (all descriptions too vague)

**Step 6: Generate Corrections**
- Fix headers type from dict to Optional[Dict[str, str]]
- Improve all parameter descriptions to be more specific
- Add default value information
- Summary: Type mismatch for headers and all descriptions too vague

**REQUIRED JSON OUTPUT:**
You MUST respond with ONLY this JSON structure. No other text.

```json
{
  "reasoning": {
    "signature_parameters": ["list of parameter names from constructor"],
    "docstring_parameters": ["list of parameter names from docstring"],
    "missing_params_from_docstring": ["parameters in constructor but not docstring"],
    "extra_params_in_docstring": ["parameters in docstring but not constructor"],
    "incorrect_param_descriptions": ["parameters with vague/unhelpful descriptions"]
  },
  "parameter_names_are_correct": true_or_false,
  "parameter_types_are_correct": true_or_false,
  "parameter_descriptions_are_correct": true_or_false,
  "corrected_class_docstring": {
    "correct_class_description": "One sentence describing what the class does",
    "correct_class_arguments": [
      {
        "name": "parameter_name",
        "data_type": "parameter_type",
        "description": "what_this_parameter_does"
      }
    ]
  },
  "summary_of_findings": "Overall summary of what you found and what you fixed"
}
```

**RULES FOR GOOD CLASS DOCSTRINGS:**
- Class description: Start with a verb ("Manage database connections" not "Manages database connections")
- Parameter types: Use exact Python types (str, int, List[str], bool, Optional[int])
- Be specific: "List[str]" is better than "list"
- Focus ONLY on constructor (__init__) parameters, not other methods
- For optional parameters with defaults, mention the default value in the description
- Always exclude 'self' parameter from documentation

**CRITICAL REMINDERS:**
- Work through ALL 6 steps systematically
- If there's no docstring at all, set ALL flags to false
- Use the exact types from the constructor signature
- The corrected docstring should fix all problems you found
- Fill in the reasoning section with your step-by-step analysis
- Only document constructor parameters, never include 'self'

The class docstring is provided within <docstring> tags and the constructor is
provided within <constructor> tags.

RESPOND WITH ONLY THE JSON. NO OTHER TEXT.
"""
