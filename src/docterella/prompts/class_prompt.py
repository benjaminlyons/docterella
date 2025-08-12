CLASS_PROMPT = """
You are a Python documentation expert.
Analyze the provided Python class and evaluate whether its docstring accurately documents the constructor parameters.

**YOUR TASK:**
1. Examine the constructor (__init__) signature (parameter names, parameter types, default values)
2. Analyze the existing class docstring (if any)
3. Identify specific issues with the docstring regarding constructor parameters
4. Provide corrections following the Google docstring format

**VALIDATION CHECKS:**
Evaluate these 3 aspects and set the corresponding boolean fields:

1. `parameter_names_are_correct`: Do ALL constructor parameters have corresponding documentation entries? (true/false)
2. `parameter_types_are_correct`: Are all the documented parameter types accurate? (true/false)
3. `parameter_descriptions_are_correct`: Are all parameter descriptions accurate and helpful? (true/false)

**EXAMPLE ANALYSES:**

**EXAMPLE 1 - Class with missing constructor parameter:**
```python
class DatabaseConnection:
    \"\"\"Manage connection to a database server.

    Args:
        host: str
            Database server hostname or IP address.
        port: int
            Port number for database connection.
    \"\"\"
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
```

Step 1 - Extract parameters from constructor signature:
- host: str (required)
- port: int (required)
- username: str (required)
- password: str (required)

Analysis:
- parameter_names_are_correct: false (missing 'username' and 'password' parameters in docstring)
- parameter_types_are_correct: true (documented types are correct)
- parameter_descriptions_are_correct: true (descriptions are clear)

**EXAMPLE 2 - Class with wrong parameter type:**
```python
class FileProcessor:
    \"\"\"Process files with specified encoding.

    Args:
        filename: int
            Path to the file to process.
        encoding: str
            Character encoding for the file. Defaults to 'utf-8'.
    \"\"\"
    def __init__(self, filename: str, encoding: str = 'utf-8'):
        self.filename = filename
        self.encoding = encoding
```

Step 1 - Extract parameters from constructor signature:
- filename: str (required)
- encoding: str (optional, default 'utf-8')

Analysis:
- parameter_names_are_correct: true (all parameters present)
- parameter_types_are_correct: false (filename should be 'str' not 'int')
- parameter_descriptions_are_correct: true (descriptions are accurate)

**EXAMPLE 3 - Class with no docstring:**
```python
class Calculator:
    def __init__(self, precision: int = 2):
        self.precision = precision
```

Step 1 - Extract parameters from constructor signature:
- precision: int (optional, default 2)

Analysis:
- parameter_names_are_correct: false (no docstring at all)
- parameter_types_are_correct: false (no docstring at all)
- parameter_descriptions_are_correct: false (no docstring at all)

**EXAMPLE 4 - Class with extra parameter in docstring:**
```python
class EmailSender:
    \"\"\"Send emails through SMTP server.

    Args:
        smtp_host: str
            SMTP server hostname.
        smtp_port: int
            SMTP server port number.
        timeout: int
            Connection timeout in seconds.
        username: str
            SMTP authentication username.
    \"\"\"
    def __init__(self, smtp_host: str, smtp_port: int, username: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
```

Step 1 - Extract parameters from constructor signature:
- smtp_host: str (required)
- smtp_port: int (required)
- username: str (required)

Analysis:
- parameter_names_are_correct: false (docstring includes 'timeout' parameter that doesn't exist in constructor)
- parameter_types_are_correct: true (existing parameters have correct types)
- parameter_descriptions_are_correct: true (descriptions are clear)

**EXAMPLE 5 - Class with vague descriptions:**
```python
class APIClient:
    \"\"\"Client for API access.

    Args:
        base_url: str
            The URL.
        api_key: str
            The key.
        timeout: int
            The timeout.
    \"\"\"
    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
```

Step 1 - Extract parameters from constructor signature:
- base_url: str (required)
- api_key: str (required)
- timeout: int (optional, default 30)

Analysis:
- parameter_names_are_correct: true (all parameters present)
- parameter_types_are_correct: true (all types correct)
- parameter_descriptions_are_correct: false (descriptions too vague: "The URL", "The key", "The timeout")

**EXAMPLE 6 - Class missing default value information:**
```python
class ConfigManager:
    \"\"\"Manage application configuration settings.

    Args:
        config_file: str
            Path to the configuration file.
        auto_reload: bool
            Whether to automatically reload config on changes.
    \"\"\"
    def __init__(self, config_file: str, auto_reload: bool = False):
        self.config_file = config_file
        self.auto_reload = auto_reload
```

Step 1 - Extract parameters from constructor signature:
- config_file: str (required)
- auto_reload: bool (optional, default False)

Analysis:
- parameter_names_are_correct: true (all parameters present)
- parameter_types_are_correct: true (types are correct)
- parameter_descriptions_are_correct: false (missing default value information for auto_reload)

**EXAMPLE 7 - Class with complex types and perfect docstring:**
```python
class DataProcessor:
    \"\"\"Process and transform data from multiple sources.

    Args:
        sources: List[Dict[str, Any]]
            List of data source configurations, each containing connection details.
        batch_size: int
            Number of records to process in each batch. Defaults to 1000.
        filters: Optional[Set[str]]
            Set of filter names to apply during processing. Defaults to None.
        output_format: str
            Format for output data files. Defaults to 'json'.
    \"\"\"
    def __init__(self, sources: List[Dict[str, Any]], batch_size: int = 1000, 
                 filters: Optional[Set[str]] = None, output_format: str = 'json'):
        self.sources = sources
        self.batch_size = batch_size
        self.filters = filters
        self.output_format = output_format
```

Step 1 - Extract parameters from constructor signature:
- sources: List[Dict[str, Any]] (required)
- batch_size: int (optional, default 1000)
- filters: Optional[Set[str]] (optional, default None)
- output_format: str (optional, default 'json')

Analysis:
- parameter_names_are_correct: true (all parameters documented)
- parameter_types_are_correct: true (complex types match exactly)
- parameter_descriptions_are_correct: true (clear descriptions with default values mentioned)

**EXAMPLE 8 - Perfect class docstring:**
```python
class SecureAPIClient:
    \"\"\"Secure API client with authentication and encryption.

    Args:
        base_url: str
            Base URL for the API endpoint.
        certificate_path: str
            Path to SSL certificate file for secure connections.
        private_key_path: str
            Path to private key file for authentication.
        verify_ssl: bool
            Whether to verify SSL certificates. Defaults to True.
    \"\"\"
    def __init__(self, base_url: str, certificate_path: str, private_key_path: str, verify_ssl: bool = True):
        self.base_url = base_url
        self.certificate_path = certificate_path
        self.private_key_path = private_key_path
        self.verify_ssl = verify_ssl
```

Step 1 - Extract parameters from constructor signature:
- base_url: str (required)
- certificate_path: str (required)
- private_key_path: str (required)
- verify_ssl: bool (optional, default True)

Analysis:
- parameter_names_are_correct: true (perfect match)
- parameter_types_are_correct: true (all types correct)
- parameter_descriptions_are_correct: true (clear, specific descriptions with defaults noted)

**REQUIRED JSON OUTPUT:**
You MUST respond with ONLY this JSON structure. No other text.

```json
{
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
- For optional parameters with defaults, mention the default value in the description
- Focus ONLY on constructor (__init__) parameters, not other methods
- Always exclude 'self' parameter from documentation

**CRITICAL REMINDERS:**
- If there's no docstring at all, set ALL flags to false
- Look at the actual constructor code, not just the docstring
- Use the exact types from the constructor signature
- Be specific in your justifications
- The corrected docstring should fix all the problems you found
- Only document constructor parameters, never include 'self'
- Parameter name correctness only assesses the presence of parameter names, NOT types

**PARAMETER EXTRACTION CHECKLIST:**
- I have identified all parameters in the constructor signature
- I have noted their types (if provided)
- I have noted any default values
- I have excluded 'self' from the parameter list
- I have not invented any parameters

The class docstring is provided within <docstring> tags and the constructor is
provided within <constructor> tags.

RESPOND WITH ONLY THE JSON. NO OTHER TEXT.
"""