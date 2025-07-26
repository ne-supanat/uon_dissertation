import json

from system_path import SystemPath


def setup_objective(path: SystemPath):
    print("\nPlease answer the following setup questions:\n")

    print("What is the simulation's Objective?")
    input_objective = input()

    print("\nWhat is the simulation's Input / Experimental factor?")
    input_experiment_factor = input()

    print("\nWhat is the simulation's Output / Response?")
    input_response = input()

    with open(path.get_01_objective_path(), "w") as f:
        dict = {
            "objective": input_objective,
            "input": input_experiment_factor,
            "output": input_response,
        }
        f.write(json.dumps(dict, indent=4))

    print()
    print("-" * 50)
    print(f"Result saved to: '{path.get_01_objective_path()}'")


if __name__ == "__main__":
    path = SystemPath("results_4")
    setup_objective(path)
