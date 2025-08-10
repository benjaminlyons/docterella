import sys

from docterella.agent import ValidationAgent
from docterella.parser import parse_file

def main():
    filename = sys.argv[1]

    validator = ValidationAgent("llama3.1:8b-instruct-q8_0")
    results_list = parse_file(filename, validator)

    print(results_list)

if __name__ == "__main__":
    main()

