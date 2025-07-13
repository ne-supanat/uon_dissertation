import json


def display(
    problem_statement_path,
):
    print(problem_statement_path)
    # Print current progress of the system
    with open(problem_statement_path, "r") as f:
        problem_statement_raw = f.read()
        problem_statement: dict = json.loads(problem_statement_raw)
        print(f"\nLoading Stage 1 data from: '{problem_statement_path}'\n")
        print("---")
        print(f'Problem statement: {problem_statement["problem"]}')
        print(f'Input/Experimental factor: {problem_statement["input"]}')
        print(f'Output/Response: {problem_statement["output"]}')
        print("---\n")
