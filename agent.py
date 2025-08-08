import json
import ollama
import ast
import astor

from docterella.output import DocstringValidation

system_prompt = """
You are an extremely detail oriented expert in Python. You are tasked with
reading Python functions and evaluating the accuracy of the function
docstring. You need to identify the following things, and provide output in the given JSON format.

    1. All arguments accepted by the function have documentation. If so, set the `docstring_argument_names_match_function_signature` value to True.
    2. Each argument listed the documentation has the correct type. If so, set the `docstring_argument_types_are_correct` value to True.
    3. All arguments in the documentation are accepted by the function. If so, set the `docstring_arguments_are_accepted` value to True.
    4. The description of each argument in the documentation is accurate. If so, set the `docstring_argument_descriptions_are_correct` value to True.
    5. If the function returns a value, then the documentation specifies the return type. If so, then set the `has_accurate_return_type` value to True.

Provide an updated docstring that resolves all identified issues using the `corrected_function_docstring` field. It should contain the following at a minimum:

    1. Provide a one-line summary description of the function in the `correct_function_description` value.
    2. For each parameter, specified the correct parameter name, data type, and one-line description.
    3. For the return value, specify the data_type and provide a oneline description in the `correct_function_return_values` value.

Finally, provide an extremely detailed overview of your findings and reasoning in the summary field. Provide all output as JSON.
"""

with open("docstring_errors.py") as f:
    content = f.read()

parsed_content = ast.parse(content)
for node in ast.walk(parsed_content):

    if not isinstance(node, ast.FunctionDef):
        continue

    print(astor.to_source(node))

    docstring = ast.get_docstring(node)

    # TODO: Check this works with null docstring
    # if docstring:
    #     node.body = node.body[1:]

    source = astor.to_source(node)

    prompt = (
        f"{system_prompt}\n"
        f"<code>{source}</code>\n"
    )

    result = ollama.generate(
        model='llama3.1:8b-instruct-q8_0',
        prompt=prompt,
        format=DocstringValidation.model_json_schema(),
        options={'temperature': 0},
    )


    print(json.dumps(json.loads(result["response"]), indent=4))

