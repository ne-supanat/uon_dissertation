import json


def define_problem_statement(result_path):
    print("\nPlease answer the following setup questions:\n")

    print("What is the simulation's problem statement?")
    input_problem_statement = input()

    print("\nWhat is the simulation's input/experimental factor?")
    input_experiment_factor = input()

    print("\nWhat is the simulation's output/response?")
    input_response = input()

    with open(result_path, "w") as f:
        dict = {
            "problem": input_problem_statement,
            "input": input_experiment_factor,
            "output": input_response,
        }
        f.write(json.dumps(dict, indent=4))

    print(f"\nResult saved to: '{result_path}'")


if __name__ == "__main__":
    results_path = "abm_analysis/results_1"
    problem_statement_path = results_path + "/problem_statement.txt"

    define_problem_statement(problem_statement_path)
