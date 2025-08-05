import json
from tabulate import tabulate, SEPARATING_LINE

from models.response_models import ScopeThemeCode, Scenario

from system_path import SystemPath

# TODO: add example output


def display_header():
    print("\nCurrent progress")


def topic_outline_progress(path: SystemPath):
    str = "-" * 50 + "\n"
    with open(path.get_01_topic_path(), "r") as f:
        content = f.read()
        str += f"Model's Topic:\n"
        str += content
        str += "\n\n"

    with open(path.get_01_outline_path(), "r") as f:
        problem_statement_raw = f.read()
        problem_statement: dict = json.loads(problem_statement_raw)
        str += f"Model's Objective:" + "\n"
        str += problem_statement["objective"] + "\n"
        str += "\n"
        str += f"Model's Experimental Factors (Input):" + "\n"
        str += problem_statement["input"] + "\n"
        str += "\n"
        str += f"Model's Response (Output):" + "\n"
        str += problem_statement["output"] + "\n"

    return str


def eabss_scope_progress(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "EABSS Scope model:\n"
    with open(path.get_02_eabss_scope_path(), "r") as f:
        scope_raw = f.read()
        scope: dict = json.loads(scope_raw)

        for key in scope.keys():
            component_name = ScopeThemeCode.get_component_name_from_key(key)

            str += f"Component: {component_name}"

            for item in scope[key]:
                str += f"\n - Element: {item["element"]}"
                str += f"\n   Description: {item["description"]}"
            str += "\n\n"
    return str


def eabss_scope_progress_table(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "EABSS Components:\n"
    with open(path.get_02_eabss_scope_path(), "r") as f:
        scope_raw = f.read()
        scope: dict = json.loads(scope_raw)

        table = []
        for key in scope.keys():
            component_name = ScopeThemeCode.get_component_name_from_key(key)

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
    # Example output
    # ---------------------
    # Scenarios:
    # Scenario 1: It is friday night. How likely are you to...
    # Actions: Stay at home, Go to party, Go to restaurant

    str = "-" * 50 + "\n"
    str += "Scenarios:"
    with open(path.get_04_scenario_path(), "r") as f:
        content = f.read()
        scenarios: list[Scenario] = [
            Scenario.model_validate_json(json.dumps(scenario_raw))
            for scenario_raw in json.loads(content)
        ]

    for i, scenario in enumerate(scenarios):
        str += f"\nScenario {i+1}: {scenario.scenario}"
        str += f"\nActions: {', '.join([action for action in scenario.actions])}"
        str += "\n"

    return str


def profile_progess(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "{:<25} {:<30}".format(
        "Profiles", f": saved to '{path.get_05_profiles_path()}'"
    )

    return str


def ground_truth_progess(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "{:<25} {:<30}".format(
        "Ground truth", f": saved to '{path.get_06_scenario_ground_truth_path()}'"
    )
    return str


def profile_scenario_answer_progess(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "{:<25} {:<30}".format(
        "Scenario answers",
        f": saved to '{path.get_06_profile_scenario_answers_path()}'",
    )

    return str


def profile_answer_table_progess(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "Profile answer table:\n"

    # Example output
    # ---------------------
    # File: data/travel_profile_txt/Pennsylvania2.txt
    # Archetype: Eco-Conscious Commuter
    # Scenario 1: scenario1's text
    # =======  =========  =========
    # Action1   Action2   Action3
    # =======  =========  =========
    #   0.3       0.3       0.4
    # =======  =========  =========

    with open(path.get_06_profile_scenario_answers_path()) as f:
        content = f.read()
        all_profile_answer = json.loads(content)

    for profile_answer in all_profile_answer:
        str += f"File: {profile_answer["file"]}\n"
        str += f"Archetype: {profile_answer["archetype"]}\n"

        for i, scenario in enumerate(profile_answer["scenarios"]):
            str += f'Scenario {i+1}: {scenario["scenario"]}\n'
            str += tabulate(
                [scenario["action_probs"]], scenario["actions"], tablefmt="rst"
            )
            str += "\n\n"

    return str


def decision_probability_table_progess(path: SystemPath):
    str = "-" * 50 + "\n"
    str += "Decision probability table:\n"

    # Example output
    # ---------------------
    # Scenario 1: scenario1's text
    # ==========  =======  =========  =========
    # Archetype   Action1   Action2   Action3
    # ==========  =======  =========  =========
    # Archetype1    0.3       0.3       0.4
    # Archetype2    0.3       0.3       0.4
    # Archetype3    0.3       0.3       0.4
    # ==========  =======  =========  =========

    with open(path.get_06_decision_probability_path()) as f:
        content = f.read()
        decision_probability = json.loads(content)

    for i, scenario in enumerate(decision_probability):
        rows = []

        for archetype, action_probs in scenario["archetype_action_probs"].items():
            rows.append([archetype] + action_probs)

        table = tabulate(
            rows, headers=["Archetype"] + scenario["actions"], tablefmt="rst"
        )

        str += f"Scenario {int(i)+1}: {scenario['scenario']}\n"
        str += f"{table}\n"
        str += f"\n"

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
    # print(topic_outline_progress(path))
    # print(eabss_scope_progress(path))
    # print(eabss_scope_progress_table(path))
    # print(diagram_header())

    # print(eabss_usecase_diagrams_progess(path))
    # print(eabss_diagrams_progess(path))
    # print(archetype_progess(path))
    # print(attribute_progess(path))
    # print(scenario_progess(path))

    # print(profile_progess(path))
    # print(profile_scenario_answer_progess(path))
    # print(ground_truth_progess(path))
    print(profile_answer_table_progess(path))
    # print(decision_probability_table_progess(path))
    # print(simulation_script_progess(path))
    # print()
    # print(model_output_progess(path))
    # print(visualisation_template_progess(path))
    # print(visualisation_analysis_progess(path))
    # print()
