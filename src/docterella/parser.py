import ast

def parse_file(filepath, validator):
    content = read_file(filepath)
    parsed_content = ast.parse(content)

    results_list = []
    for node in ast.walk(parsed_content):
        if isinstance(node, ast.FunctionDef):
            result = validator.validate_function(node)
            results_list.append(result)
    return results_list

def read_file(filepath):
    with open(filepath) as f:
        content = f.read()

    return content

    
