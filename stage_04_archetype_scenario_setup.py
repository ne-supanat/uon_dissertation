import json
import re
from google.genai.types import GenerateContentResponse
from tabulate import tabulate

import display_result
from system_path import SystemPath
import llm
from models.response_models import ScenarioList


def design_profile_n_scenario(path: SystemPath):
    setup_profile_attribute(path)
    setup_archetype(path)
    setup_scenarios(path)


def setup_profile_attribute(path: SystemPath):
    response = generate_potential_profile_attributes(path)

    print("-" * 50)
    print("Define profile attributes.")
    print("-" * 50)

    print(
        f"""
Example:
    Please enter the number of attributes: 2
    Enter Attribute 1 text: Age
    Enter Attribute 2 text: Occupation

{"-"*50}
"""
    )

    print()
    print("Suggestions:")
    for e in response.parsed:
        print(f"    - {e}")

    while True:
        try:
            attributes_size = int(input("Please enter the number of attributes: "))
            break
        except:
            pass

    attributes = []
    for i in range(attributes_size):
        while True:
            attributes_text = input(f"Enter Attribute {i+1} text: ")
            if attributes_text.strip() != "":
                break
        attributes.append(attributes_text.strip())

    # Example output
    # ----------------
    # Age
    # Occupation

    with open(path.get_04_attributes_path(), "w") as f:
        f.write(f'{'\n'.join(attributes)}')

    print()
    print("-" * 50)
    print(f"Profile attributes saved to: '{path.get_04_attributes_path()}'")


def generate_potential_profile_attributes(path: SystemPath) -> GenerateContentResponse:
    with open(path.get_03_eabss_main_actor_path(), "r") as f:
        main_actor = f.read()

    prompt = f"""
Based on the scope
{display_result.eabss_scope_result(path)}

Please suggest {3} potential {main_actor} attributes.

For example: Race, Age, Occupation
"""

    response = llm.generate_content(prompt, response_schema=list[str])
    return response


def setup_archetype(path: SystemPath):
    with open(path.get_04_attributes_path()) as f:
        attributes = f.read().strip().splitlines()

    response = generate_potential_archetype(path, attributes)

    print("-" * 50)
    print("Define Agent Archetypes")
    print("-" * 50)

    print(
        f"""
Example:
    Please enter number of archetypes: 3
    Enter Archetype 1: Introvert
    Enter Archetype 2: Ambivert
    Enter Archetype 2: Extrovert

{"-"*50}
"""
    )

    print()
    print("Suggestions:")
    for e in response.parsed:
        print(f"    - {e}")

    while True:
        try:
            answer_size = int(input("Please enter the number of archetypes: ").strip())
            break
        except:
            pass

    answers = []
    for i in range(answer_size):
        while True:
            answers_text = input(f"Enter Archetype {i+1}: ")
            if answers_text.strip() != "":
                break
        answers.append(answers_text)

    ## Save archetypes
    with open(path.get_04_archetypes_path(), "w") as f:
        f.write("\n".join(answers))

    print()
    print("-" * 50)
    print(f"Archetype saved at: '{path.get_04_archetypes_path()}'")

    ## Update Archeype model
    model_archetype_path = "models/archetypes.py"

    # Example output
    # ----------------
    # import enum
    #
    # class Archetype(enum.Enum):
    #     ExampleArchetype1 = "Example Archetype 1"
    #     ExampleArchetype2 = "Example Archetype 2"

    content = "import enum\n\nclass Archetype(enum.Enum):\n"
    for item in answers:
        content += f"""\t{"".join([word.lower().capitalize() for word in sanitise_name(item).split(" ")])} = "{item}"\n"""

    with open(model_archetype_path, "w") as f:
        f.write(content)

    print(f"System's Archetype model updated at: '{model_archetype_path}'")


def generate_potential_archetype(
    path: SystemPath, attributes: list[str]
) -> GenerateContentResponse:
    with open(path.get_03_eabss_main_actor_path(), "r") as f:
        main_actor = f.read()

    prompt = f"""
Based on the scope
{display_result.eabss_scope_result(path)}

And attribute
{", ".join(attributes)}

Please suggest {3} potential {main_actor} archetypes.
For example: Introvert, Ambivert, Extrovert
"""

    response = llm.generate_content(prompt, response_schema=list[str])
    return response


def setup_scenarios(path: SystemPath):
    print("-" * 50)
    print("Design scenario and actions.")
    print(
        "Note: the scenario and actions will be used to generate scenario actions probability"
    )

    print()
    print("Final Result Example: It is Friday night. How likely are you to...")

    header = (["Archetype", "Stay at home", "Go to party", "Go to restaurant"],)
    table = [
        ["Introvert", "0.7", "0.1", "0.2"],
        ["Ambivert", "0.3", "0.3", "0.4"],
        ["Extrovert", "0.05", "0.8", "0.15"],
    ]

    print(
        tabulate(
            table,
            headers=header,
            tablefmt="rst",
        )
    )

    # Suggestion
    response = generate_scenario_suggestion(path)
    scenario_suggestion: ScenarioList = response.parsed

    print()
    print("Suggestions:")
    print("-" * 50)
    for i, suggestion in enumerate(scenario_suggestion.scenarios):
        print(f"Scenario {i+1}: {suggestion.scenario}")
        print(f"Actions:")
        print(f"{'\n'.join([f'  {action}' for action in suggestion.actions])}")
        print()

    # Add scenario
    add_scenarios(path)
    print()


def add_scenarios(path: SystemPath):
    print("-" * 50)
    scenario_dict: dict = {}

    i = 0
    done = False
    while not done:
        print()
        # Add Scenario
        while True:
            scenario = input(f"Enter Scenario {i+1} text: ")
            if scenario.strip() != "":
                break

        print()

        # Add Scenario's actions
        answer_size = 0
        while answer_size < 2:
            try:
                answer_size = int(
                    input(
                        "Please enter number of answer actions (more than 1): "
                    ).strip()
                )
            except:
                pass

        actions = []
        for j in range(answer_size):
            while True:
                answers_text = input(f"Enter Actions {j+1}: ")
                if answers_text.strip() != "":
                    break
            actions.append(answers_text)

        # Store scenario
        scenario_dict[i] = {"scenario": scenario, "actions": actions}

        # Ask to add more scenario
        add_more = None
        while add_more not in ["y", "n"]:
            add_more = input(f"\nDo you want to add more scenario? (y/n): ").lower()
        done = add_more == "n"
        i += 1

    # Save scenarios
    with open(path.get_04_scenario_path(), "w") as f:
        f.write(json.dumps(list(scenario_dict.values()), indent=4))

    print()
    print("-" * 50)
    print(f"Scenario saved to: '{path.get_04_scenario_path()}'")


def generate_scenario_suggestion(path: SystemPath) -> GenerateContentResponse:
    prompt = f"""
Based on the model's scope
{display_result.eabss_scope_result(path)}

Please suggest {3} scenarios with no more than {3} actions that help identify how each archetype behaves.
Each scenario should designed to capture action preferences.

Example:
    Scenario: It is Friday night. How likely are you to...
    Actions: Stay at home, Go to party, Go to restaurant
"""
    response = llm.generate_content(prompt, response_schema=ScenarioList)
    return response


def sanitise_name(str: str):
    return re.sub("[^a-zA-Z0-9 \n.]", " ", str)  # remove special character


if __name__ == "__main__":
    path = SystemPath("travel")
    design_profile_n_scenario(path)
