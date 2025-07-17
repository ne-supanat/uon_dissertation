import os
import json
import csv
from tabulate import tabulate, SEPARATING_LINE

from response_models import KeyComponents
from models.scenario_choices import ScenarioChoice


def display_header():
    print("\nCurrent progress")


def objective_statement_progress(
    objective_statement_path,
):
    str = "-" * 50 + "\n"
    with open(objective_statement_path, "r") as f:
        problem_statement_raw = f.read()
        problem_statement: dict = json.loads(problem_statement_raw)
        str += f'Objective: {problem_statement["objective"]}\n'
        str += f'Input/Experimental factor: {problem_statement["input"]}\n'
        str += f'Output/Response: {problem_statement["output"]}'

    return str


def eabss_components_progress(
    eabss_scope_path,
):
    str = "-" * 50 + "\n"
    with open(eabss_scope_path, "r") as f:
        scope_raw = f.read()
        scope: dict = json.loads(scope_raw)

        table = []
        for key in scope.keys():
            component = KeyComponents.get_component_names()[
                KeyComponents.get_component_keys().index(key)
            ]

            for item in scope[key]:
                elemenet = item["code"]
                table.append([component, elemenet])

    str += tabulate(table, headers=["Component", "Element"], tablefmt="rst")
    return str


def eabss_diagrams_progess(
    eabss_usecase_diagram_path,
    eabss_activity_diagram_path,
    eabss_state_transition_diagram_path,
    eabss_interaction_diagram_path,
):
    str = "-" * 50 + "\n"
    str += "You can view EABSS diagrams using mermaid.js"
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
        str += "\n  {:<25} {:<30}".format(name, f": saved to '{path}'")

    return str


def archetype_progess(archetype_path):
    str = "-" * 50 + "\n"
    str += "Archetypes:"
    with open(archetype_path, "r") as f:
        content = f.read()

    for i, archetype in enumerate(content.strip().split("\n")):
        str += f"\n{i+1}. {archetype}"

    return str


def scenario_progess(scenario_questions_path, scenario_choices_path):
    str = "-" * 50 + "\n"
    str += "Scenario questions:"
    with open(scenario_questions_path, "r") as f:
        content = f.read()

    for i, question in enumerate(content.split("\n")):
        str += f"\n{i+1}. {question}"

    str += "\n" + "-" * 50 + "\n"
    str += "Scenario answer choices:"
    with open(scenario_choices_path, "r") as f:
        content = f.read()

    for i, choice in enumerate(content.strip().split("\n")):
        str += f"\n{i+1}. {choice}"

    return str


def profile_progess(profiles_path):
    str = "-" * 50 + "\n"
    str += "{:<25} {:<30}".format("Profiles", f": saved to '{profiles_path}'")

    return str


def profile_scenario_answer_progess(profile_scenario_answers_path):
    str = "-" * 50 + "\n"
    str += "{:<25} {:<30}".format(
        "Scenario answers", f": saved to '{profile_scenario_answers_path}'"
    )

    return str


def decision_probability_table_progess(decision_probability_path):
    str = "-" * 50 + "\n"
    with open(decision_probability_path) as f:
        reader = csv.reader(f, delimiter=";")

        headers = ["Question", "Archetype"]
        headers += [choice.value for choice in ScenarioChoice]

        rows = []
        current_question = ""
        for row in reader:
            if current_question == row[0]:
                row[0] = ""  # Hide repeated question
            else:
                if current_question != "":
                    rows.append(SEPARATING_LINE)
                current_question = row[0]

            rows.append(row)

        str += tabulate(rows, headers=headers, tablefmt="rst")

    return str


def profile_scenario_answer_progess(simulation_script_path):
    str = "-" * 50 + "\n"
    str += "{:<25} {:<30}".format(
        "Simulation script", f": saved to '{simulation_script_path}'"
    )

    return str


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
    decision_probability_path = os.path.join(results_path, "scenario_probability.csv")
    simulation_script_path = os.path.join(results_path, "simulation_script.txt")

    display_header()
    print(objective_statement_progress(problem_statement_path))
    print(eabss_components_progress(eabss_components_path))
    print(
        eabss_diagrams_progess(
            eabss_usecase_diagram_path,
            eabss_activity_diagram_path,
            eabss_state_transition_diagram_path,
            eabss_interaction_diagram_path,
        )
    )
    print(archetype_progess(archetype_path))
    print(scenario_progess(scenario_questions_path, scenario_choices_path))
    print(profile_progess(profiles_path))
    print(profile_scenario_answer_progess(profile_scenario_answers_path))
    print(decision_probability_table_progess(decision_probability_path))
    print(profile_scenario_answer_progess(simulation_script_path))
    print()
