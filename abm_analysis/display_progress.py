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
    print("You can view EABSS diagrams using mermaid.js")
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
        print("  {:<25} {:<30}".format(name, f": saved to '{path}'"))


def display_archetype(archetype_path):
    print("-" * 50)
    print("Archetypes:")
    with open(archetype_path, "r") as f:
        content = f.read()

    for i, archetype in enumerate(content.strip().split("\n")):
        print(f"{i+1}. {archetype}")


def display_scenario(scenario_questions_path, scenario_choices_path):
    print("-" * 50)
    print("Scenario questions:")
    with open(scenario_questions_path, "r") as f:
        content = f.read()

    for i, question in enumerate(content.split("\n")):
        print(f"{i+1}. {question}")

    print()
    print("Scenario answer choices:")
    with open(scenario_choices_path, "r") as f:
        content = f.read()

    for i, choice in enumerate(content.strip().split("\n")):
        print(f"{i+1}. {choice}")


def display_profile(profiles_path):
    print("-" * 50)
    print("{:<25} {:<30}".format("Profiles", f": saved to '{profiles_path}'"))


def display_profile_scenario_answer(profile_scenario_answers_path):
    print("-" * 50)
    print(
        "{:<25} {:<30}".format(
            "Scenario answers", f": saved to '{profile_scenario_answers_path}'"
        )
    )


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
    archetype_path = os.path.join(results_path, "archetype.txt")
    scenario_questions_path = os.path.join(results_path, "scenario_questions.txt")
    scenario_choices_path = os.path.join(results_path, "scenario_choices.txt")
    profiles_path = os.path.join(results_path, "profiles.txt")
    profile_scenario_answers_path = os.path.join(
        results_path, "profile_scenario_answers.csv"
    )

    display_header()
    display_problem_statement(problem_statement_path)
    display_eabss_components(eabss_components_path)
    display_eabss_diagrams(
        eabss_usecase_diagram_path,
        eabss_activity_diagram_path,
        eabss_state_transition_diagram_path,
        eabss_interaction_diagram_path,
    )
    display_archetype(archetype_path)
    display_scenario(scenario_questions_path, scenario_choices_path)
    display_profile(profiles_path)
    display_profile_scenario_answer(profile_scenario_answers_path)
