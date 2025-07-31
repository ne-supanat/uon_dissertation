import os
import json
import csv
from tabulate import tabulate, SEPARATING_LINE

from models.response_models import ScopeThemeCode
from models.scenario_choices import ScenarioChoice

from system_path import SystemPath

# TODO: add example output


def display_header():
    print("\nCurrent progress")


def display_topic_outline_progress(path: SystemPath):
    print("-" * 50)
    with open(path.get_01_topic_path(), "r") as f:
        content = f.read()
        print(f"Model's Topic:")
        print(content)
        print()

    with open(path.get_01_outline_path(), "r") as f:
        problem_statement_raw = f.read()
        problem_statement: dict = json.loads(problem_statement_raw)
        print(f"Model's Objective:")
        print(problem_statement["objective"])
        print()
        print(f"Model's Experimental Factors(Input):")
        print(problem_statement["input"])
        print()
        print(f"Model's Response:")
        print(problem_statement["output"])
        print()


def eabss_components_progress(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "EABSS Components:\n"
    with open(path.get_02_eabss_scope_path(), "r") as f:
        scope_raw = f.read()
        scope: dict = json.loads(scope_raw)

        for key in scope.keys():
            component_name = ScopeThemeCode.get_component_names()[
                ScopeThemeCode.get_component_keys().index(key)
            ]

            str += f"Component: {component_name}"

            for item in scope[key]:
                str += f"\n - Element: {item["element"]}"
                str += f"\n   Description: {item["description"]}"
            str += "\n\n"
    return str


def eabss_components_progress_table(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "EABSS Components:\n"
    with open(path.get_02_eabss_scope_path(), "r") as f:
        scope_raw = f.read()
        scope: dict = json.loads(scope_raw)

        table = []
        for key in scope.keys():
            component_name = ScopeThemeCode.get_component_names()[
                ScopeThemeCode.get_component_keys().index(key)
            ]

            for item in scope[key]:
                elemenet = item["element"]
                table.append([component_name, elemenet])

    str += tabulate(table, headers=["Component", "Element"], tablefmt="rst")
    return str


def diagram_header():
    str = "-" * 50 + "\n"
    str += "You can view EABSS diagrams using mermaid.js"
    return str


def eabss_usecase_diagrams_progess(path: SystemPath):
    return "  {:<25} {:<30}".format(
        "Use case diagram", f": saved to '{path.get_03_eabss_usecase_diagram_path()}'"
    )


def eabss_diagrams_progess(path: SystemPath):
    strs = []
    for name, path in zip(
        [
            "Activity diagram",
            "State transition diagram",
            "Interaction diagram",
            "Class diagram",
        ],
        [
            path.get_03_eabss_class_diagram_path(),
            path.get_03_eabss_activity_diagram_path(),
            path.get_03_eabss_state_diagram_path(),
            path.get_03_eabss_interaction_diagram_path(),
        ],
    ):
        strs.append("  {:<25} {:<30}".format(name, f": saved to '{path}'"))

    return "\n".join(strs)


def display_stage04(path: SystemPath):
    print(archetype_progess(path))
    print(attribute_progess(path))
    print(scenario_progess(path))


def archetype_progess(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "Archetypes:"
    with open(path.get_04_archetypes_path(), "r") as f:
        content = f.read()

    for i, archetype in enumerate(content.strip().splitlines()):
        str += f"\n{i+1}. {archetype}"

    return str


def attribute_progess(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "Profile attributes:"
    with open(path.get_04_attributes_path(), "r") as f:
        content = f.read()

    for i, attribute in enumerate(content.strip().splitlines()):
        str += f"\n{i+1}. {attribute}"

    return str


def scenario_progess(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "Scenario answer choices:"
    with open(path.get_04_scenario_choices_path(), "r") as f:
        content = f.read()
    for i, choice in enumerate(content.strip().splitlines()):
        str += f"\n{i+1}. {choice}"

    str += "\n" + "-" * 50 + "\n"
    str += "Scenario questions:"
    with open(path.get_04_scenario_questions_path(), "r") as f:
        content = f.read()
    for i, question in enumerate(content.splitlines()):
        str += f"\n{i+1}. {question}"

    return str


def ground_truth_progess(path: SystemPath):
    # Example output
    # ---------------------
    # Scenario ground truth:
    #
    # Question1:
    # archetype1: choice, choice
    # archetype2: choice, choice
    #
    # Question2:
    # archetype1: choice, choice
    # archetype2: choice, choice

    str = "-" * 50 + "\n"
    str += "Scenario ground truth:\n\n"

    with open(path.get_04_archetypes_path(), "r") as f:
        content = f.read()
        archetypes = content.strip().splitlines()

    with open(path.get_06_scenario_ground_truth_path(), "r") as f:
        ground_truth_list: list = json.loads(f.read())

    max_lenght = len(max(archetypes, key=len))

    blocks = []
    for i, ground_truth in enumerate(ground_truth_list):
        rows = []
        rows.append(f"Question {i+1}: {ground_truth['question']}")
        for key, item in ground_truth["answer"].items():
            rows.append(f"  {key:<{max_lenght+2}}: {", ".join(item)}")
        blocks.append("\n".join(rows))
    str += "\n\n".join(blocks)

    return str


def profile_progess(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "{:<25} {:<30}".format(
        "Profiles", f": saved to '{path.get_05_profiles_path()}'"
    )

    return str


def profile_scenario_answer_progess(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "{:<25} {:<30}".format(
        "Scenario answers",
        f": saved to '{path.get_06_profile_scenario_answers_path()}'",
    )

    return str


def decision_probability_table_progess(path: SystemPath):
    str = "-" * 50 + "\n"
    with open(path.get_06_decision_probability_path()) as f:
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


def simulation_script_progess(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "{:<25} {:<30}".format(
        "Simulation script", f": saved to '{path.get_07_simulation_script_path()}'"
    )

    return str


def model_output_progess(output_path):
    str = "-" * 50 + "\n"
    str += "{:<35} {:<30}".format(
        "Model output",
        f": found at '{output_path}'",
    )

    return str


def visualisation_template_progess(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "{:<35} {:<30}".format(
        "Visualisation template reasoning",
        f": saved to '{path.get_09_visualisation_template_think_path()}'",
    )
    str += "\n"
    str += "{:<35} {:<30}".format(
        "Visualisation template script",
        f": saved to '{path.get_09_visualisation_template_path()}'",
    )

    return str


def visualisation_analysis_progess(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "{:<35} {:<30}".format(
        "Visualisation analysis ",
        f": saved to '{path.get_10_visualisation_analysis_path()}'",
    )

    return str


if __name__ == "__main__":
    path = SystemPath("travel")

    # display_header()
    print(display_topic_outline_progress(path))
    # print(eabss_components_progress(path))
    # print(eabss_components_progress_table(path))
    # print(diagram_header())

    # print(eabss_usecase_diagrams_progess(path))
    # print(eabss_diagrams_progess(path))
    # print(archetype_progess(path))
    # print(attribute_progess(path))
    # print(scenario_progess(path))

    # print(profile_progess(path))
    # print(profile_scenario_answer_progess(path))
    # print(decision_probability_table_progess(path))
    # print(simulation_script_progess(path))
    # print()
    # print(model_output_progess(path))
    # print(visualisation_template_progess(path))
    # print(visualisation_analysis_progess(path))
    # print()
    # print(ground_truth_progess(path))
