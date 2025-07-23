import os
import json
import csv
from tabulate import tabulate, SEPARATING_LINE

from models.response_models import KeyComponents
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


def diagram_header():
    str = "-" * 50 + "\n"
    str += "You can view EABSS diagrams using mermaid.js"
    return str


def eabss_usecase_diagrams_progess(
    eabss_usecase_diagram_path,
):
    return "  {:<25} {:<30}".format(
        "Use case diagram", f": saved to '{eabss_usecase_diagram_path}'"
    )


def eabss_diagrams_progess(
    eabss_activity_diagram_path,
    eabss_state_transition_diagram_path,
    eabss_interaction_diagram_path,
    eabss_class_diagram_path,
):
    strs = []
    for name, path in zip(
        [
            "Activity diagram",
            "State transition diagram",
            "Interaction diagram",
            "Class diagram",
        ],
        [
            eabss_activity_diagram_path,
            eabss_state_transition_diagram_path,
            eabss_interaction_diagram_path,
            eabss_class_diagram_path,
        ],
    ):
        strs.append("  {:<25} {:<30}".format(name, f": saved to '{path}'"))

    return "\n".join(strs)


def archetype_progess(archetype_path):
    str = "-" * 50 + "\n"
    str += "Archetypes:"
    with open(archetype_path, "r") as f:
        content = f.read()

    for i, archetype in enumerate(content.strip().splitlines()):
        str += f"\n{i+1}. {archetype}"

    return str


def attribute_progess(attribute_path):
    str = "-" * 50 + "\n"
    str += "Profile attributes:"
    with open(attribute_path, "r") as f:
        content = f.read()

    for i, attribute in enumerate(content.strip().splitlines()):
        str += f"\n{i+1}. {attribute}"

    return str


def scenario_progess(scenario_questions_path, scenario_choices_path):
    str = "-" * 50 + "\n"
    str += "Scenario answer choices:"
    with open(scenario_choices_path, "r") as f:
        content = f.read()
    for i, choice in enumerate(content.strip().splitlines()):
        str += f"\n{i+1}. {choice}"

    str += "\n" + "-" * 50 + "\n"
    str += "Scenario questions:"
    with open(scenario_questions_path, "r") as f:
        content = f.read()
    for i, question in enumerate(content.splitlines()):
        str += f"\n{i+1}. {question}"

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


def model_output_progess(output_path):
    str = "-" * 50 + "\n"
    str += "{:<35} {:<30}".format(
        "Model output",
        f": found at '{output_path}'",
    )

    return str


def visualisation_template_progess(
    simulation_script_think_path, simulation_script_path
):
    str = "-" * 50 + "\n"
    str += "{:<35} {:<30}".format(
        "Visualisation template reasoning",
        f": saved to '{simulation_script_think_path}'",
    )
    str += "\n"
    str += "{:<35} {:<30}".format(
        "Visualisation template script",
        f": saved to '{simulation_script_path}'",
    )

    return str


def visualisation_analysis_progess(visualisation_analysis):
    str = "-" * 50 + "\n"
    str += "{:<35} {:<30}".format(
        "Visualisation analysis ",
        f": saved to '{visualisation_analysis}'",
    )

    return str


if __name__ == "__main__":
    results_path = "results_4"
    problem_statement_path = os.path.join(results_path, "01_objective.txt")
    eabss_components_path = os.path.join(results_path, "02_eabss_scope.txt")
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
    eabss_class_diagram_path = os.path.join(results_path, "eabss_class_diagram.txt")

    archetype_path = os.path.join(results_path, "04_archetype.txt")
    attribute_path = os.path.join(results_path, "04_attribute.txt")
    scenario_questions_path = os.path.join(results_path, "04_scenario_questions.txt")
    scenario_choices_path = os.path.join(results_path, "04_scenario_choices.txt")
    profiles_path = os.path.join(results_path, "05_profiles.txt")
    profile_scenario_answers_path = os.path.join(
        results_path, "06_profile_scenario_answers.csv"
    )
    decision_probability_path = os.path.join(
        results_path, "06_scenario_probability.csv"
    )
    simulation_script_path = os.path.join(results_path, "07_simulation_script.txt")

    # Output analysis
    model_output_path = "./output.csv"
    visualisation_template_think_path = os.path.join(
        results_path, "09_visualisation_template_think.txt"
    )
    visualisation_template_path = os.path.join(
        results_path, "09_visualisation_template.txt"
    )
    visualisation_analysis = os.path.join(results_path, "10_visualisation_analysis.txt")

    display_header()
    print(objective_statement_progress(problem_statement_path))
    print(eabss_components_progress(eabss_components_path))
    print(diagram_header())

    print(
        eabss_usecase_diagrams_progess(
            eabss_usecase_diagram_path,
        )
    )
    print(
        eabss_diagrams_progess(
            eabss_activity_diagram_path,
            eabss_state_transition_diagram_path,
            eabss_interaction_diagram_path,
            eabss_class_diagram_path,
        )
    )
    print(archetype_progess(archetype_path))
    print(attribute_progess(attribute_path))
    print(scenario_progess(scenario_questions_path, scenario_choices_path))
    print(profile_progess(profiles_path))
    print(profile_scenario_answer_progess(profile_scenario_answers_path))
    print(decision_probability_table_progess(decision_probability_path))
    print(profile_scenario_answer_progess(simulation_script_path))
    print()
    print(model_output_progess(model_output_path))
    print(
        visualisation_template_progess(
            visualisation_template_think_path, visualisation_template_path
        )
    )
    print(visualisation_analysis_progess(visualisation_analysis))
