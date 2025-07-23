import os
import json


def define_objective_statement(objective_statement_path):
    print("\nPlease answer the following setup questions:\n")

    print("What is the simulation's Objective?")
    input_objective = input()

    print("\nWhat is the simulation's Input / Experimental factor?")
    input_experiment_factor = input()

    print("\nWhat is the simulation's Output / Response?")
    input_response = input()

    with open(objective_statement_path, "w") as f:
        dict = {
            "objective": input_objective,
            "input": input_experiment_factor,
            "output": input_response,
        }
        f.write(json.dumps(dict, indent=4))

    print()
    print("-" * 50)
    print(f"Result saved to: '{objective_statement_path}'")


if __name__ == "__main__":
    results_path = "results_2"
    objective_statement_path = os.path.join(results_path, "01_objective.txt")

    define_objective_statement(objective_statement_path)
