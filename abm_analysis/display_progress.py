import os
import json

from response_models import KeyComponents


def display_header():
    print("\nCurrent progress")


def display_problem_statement(
    problem_statement_path,
):
    with open(problem_statement_path, "r") as f:
        problem_statement_raw = f.read()
        problem_statement: dict = json.loads(problem_statement_raw)
        print("-" * 50)
        print(f'Objective: {problem_statement["objective"]}')
        print(f'Input/Experimental factor: {problem_statement["input"]}')
        print(f'Output/Response: {problem_statement["output"]}')


def display_eabss_components(
    eabss_scope_path,
):
    with open(eabss_scope_path, "r") as f:
        scope_raw = f.read()
        scope: dict = json.loads(scope_raw)
        print("-" * 50)
        print("{:<25} {:<30}".format("Component", "Element"))
        print("-" * 50)
        for key in scope.keys():
            component = KeyComponents.get_component_names()[
                KeyComponents.get_component_keys().index(key)
            ]

            for item in scope[key]:
                elemenet = item["code"]
                print("{:<25} {:<30}".format(component, elemenet))


def display_eabss_diagrams(
    eabss_usecase_diagram_path,
    eabss_activity_diagram_path,
    eabss_state_transition_diagram_path,
    eabss_interaction_diagram_path,
):
    print("-" * 50)

    for name, path in zip(
        [
            "Use case diagram",
            "Activity diagram",
            "State transition diagram",
            "Interaction diagram",
        ],
        [
            eabss_usecase_diagram_path,
            eabss_activity_diagram_path,
            eabss_state_transition_diagram_path,
            eabss_interaction_diagram_path,
        ],
    ):
        print("{:<25} {:<30}".format(name, f": saved to '{path}'"))

    # print(f"Use case diagram            :saved to '{eabss_usecase_diagram_path}'")
    # print(f"Activity diagram            :saved to '{eabss_activity_diagram_path}'")
    # print(
    #     f"State transition diagram      :saved to '{eabss_state_transition_diagram_path}'"
    # )
    # print(f"Interaction diagram         : saved to '{eabss_interaction_diagram_path}'")
    print()
    print("You can view these diagrams using mermaid.js.")


if __name__ == "__main__":
    results_folder = "abm_analysis/results_2"
    results_path = results_folder
    problem_statement_path = os.path.join(results_path, "objective.txt")
    eabss_components_path = os.path.join(results_path, "eabss_scope.txt")
    eabss_usecase_diagram_path = os.path.join(results_path, "eabss_usecase_diagram.txt")
    eabss_activity_diagram_path = os.path.join(
        results_path, "eabss_activity_diagram.txt"
    )
    eabss_state_transition_diagram_path = os.path.join(
        results_path, "eabss_state_diagram.txt"
    )
    # TODO: add transition table = os.path.join(results_path,"/eabss_state_table.txt")
    eabss_interaction_diagram_path = os.path.join(
        results_path, "eabss_interaction_diagram.txt"
    )

    print(os.path.join(results_path, "eabss_interaction_diagram.txt"))

    display_header()
    display_problem_statement(problem_statement_path)
    display_eabss_components(eabss_components_path)
    display_eabss_diagrams(
        eabss_usecase_diagram_path,
        eabss_activity_diagram_path,
        eabss_state_transition_diagram_path,
        eabss_interaction_diagram_path,
    )
