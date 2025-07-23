import json
import os
import re

import llm
from models.archetypes import Archetype
from models.scenario_choices import ScenarioChoice


def setup_archetype_attribute_scenario(
    eabss_components_path,
    archetype_path,
    attribute_path,
    scenario_questions_path,
    scenario_choices_path,
):
    setup_archetype(eabss_components_path, archetype_path)
    setup_profile_attribute(attribute_path)
    setup_scenario(scenario_questions_path, scenario_choices_path)


def setup_archetype(eabss_components_path, archetype_path):
    print("\nDefine Archetypes.")
    with open(eabss_components_path, "r") as f:
        scope_raw = f.read()
        scope: dict = json.loads(scope_raw)

    ## Save updated archetypes
    with open(archetype_path, "w") as f:
        f.write("\n".join(item["code"] for item in scope["archetypes"]))

    print()
    print("-" * 50)
    print(f"Archetype saved at: '{archetype_path}'")

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
    for item in scope["archetypes"]:
        content += f"""\t{"".join([word.lower().capitalize() for word in sanitise_name(item["code"]).split(" ")])} = "{item["code"]}"\n"""

    with open(model_archetype_path, "w") as f:
        f.write(content)

    print(f"System's Archetype model updated at: '{model_archetype_path}'")


def setup_profile_attribute(attribute_path):
    print("-" * 50)
    print("Define profile attributes.")
    print(
        f"""
- Example input -
Please enter the number of attributes: 2
Enter the attribute 1 text: Age
Enter the attribute 2 text: Occupation
{"-"*50}
"""
    )

    while True:
        try:
            attributes_size = int(input("Please enter the number of attribute: "))
            break
        except:
            pass

    attributes = []
    for i in range(attributes_size):
        while True:
            attributes_text = input(f"Enter the attribute {i+1} text: ")
            if attributes_text.strip() != "":
                break
        attributes.append(attributes_text.strip())

    # Example output
    # ----------------
    # Age
    # Occupation

    with open(attribute_path, "w") as f:
        f.write(f'{'\n'.join(attributes)}')

    print()
    print("-" * 50)
    print(f"Profile attributes saved to: '{attribute_path}'\n")


def setup_scenario(questions_path, scenario_choices_path):
    print("-" * 50)
    print("Define scenario questions and answers choices.")
    print(
        "For simplicity of the model, please use questions that can answer with the same set of choices."
    )
    print(
        f"""
- Example input -
Enter number of answer choices: 3
Choice 1: Walking
Choice 2: Cycling
Choice 3: Driving
{"-"*50}
"""
    )
    setup_scenario_choices(scenario_choices_path)

    print(
        f"""
- Example input -
Please enter the number of questions: 2
Enter the question 1 text: What is your transport mode in usual days?
Enter the question 2 text: What is your transport mode when it raining?
{"-"*50}
"""
    )
    setup_scenario_questions(questions_path)
    print()


def setup_scenario_questions(questions_path):
    while True:
        try:
            questions_size = int(input("Please enter the number of questions: "))
            break
        except:
            pass

    questions = []
    for i in range(questions_size):
        while True:
            questions_text = input(f"Enter the question {i+1} text: ")
            if questions_text.strip() != "":
                break
        questions.append(questions_text.strip())

    # Example output
    # ----------------
    # What is your transport mode in usual days?
    # What is your transport mode when it raining?

    with open(questions_path, "w") as f:
        f.write(f'{'\n'.join(questions)}')

    print()
    print("-" * 50)
    print(f"Scenario questions saved to: '{questions_path}'\n")


def setup_scenario_choices(scenario_choices_path):
    while True:
        try:
            answer_size = int(
                input("Please enter the number of answer choices: ").strip()
            )
            break
        except:
            pass

    answers = []
    for i in range(answer_size):
        while True:
            answers_text = input(f"Choice {i+1}: ")
            if answers_text.strip() != "":
                break
        answers.append(answers_text)

    ## Save scenario choices
    with open(scenario_choices_path, "w") as f:
        f.write("\n".join(answers))

    print()
    print("-" * 50)
    print(f"Scenario choices saved to: '{scenario_choices_path}''")

    ## Update Scenario choice model
    answer_choices_path = "models/scenario_choices.py"

    # Example output
    # ----------------
    # import enum
    #
    # class ScenarioChoice(enum.Enum):
    #     Choice1 = "choice1"
    #     Choice2 = "choice2"
    #     Choice3 = "choice3"

    content = "import enum\n\nclass ScenarioChoice(enum.Enum):\n"
    for item in answers:
        content += f"""\t{"".join([word.lower().capitalize() for word in sanitise_name(item).split(" ")])} = "{item}"\n"""

    with open(answer_choices_path, "w") as f:
        f.write(content)

    print(f"System's Scenario choice model updated at: '{answer_choices_path}''")


def sanitise_name(str: str):
    return re.sub("[^a-zA-Z0-9 \n.]", " ", str)  # remove special character


def create_ground_truth(scenario_questions_path, scenario_ground_truth_path):
    response = generate_synthetic_answer(scenario_questions_path)
    with open(scenario_ground_truth_path, "w") as f:
        f.write(response.text)

    print()
    print("-" * 50)
    print(f"Scenario ground truths saved to: '{scenario_ground_truth_path}'\n")


def generate_synthetic_answer(
    scenario_questions_path,
):
    with open(scenario_questions_path, "r") as f:
        content = f.read()
        questions = content.strip().splitlines()

    prompt = f"""
Archetypes are {", ".join([type.value for type in Archetype])}
Choices are {", ".join([type.value for type in ScenarioChoice])}

What archetype each choice belong (choice can be in one, some, all or none of the archetypes)

Give answers for the following questions:
{questions}

Respond in this format

{"{"}[
[[choice1,choice2],[choice3,choice4]],
[[choice1,choice2],[choice3,choice4]],
]{"}"}

which is

{"{"}[
[[Choices belong to Archetype 1 of Question 1], [Choices belong to Archetype 2 of Question 1]],
[[Choices belong to Archetype 1 of Question 2], [Choices belong to Archetype 2 of Question 2]],
]{"}"}
"""

    response = llm.generate_content(prompt, list[list[list[ScenarioChoice]]])
    return response


if __name__ == "__main__":
    results_path = "results_4"

    eabss_components_path = os.path.join(results_path, "02_eabss_scope.txt")
    archetype_path = os.path.join(results_path, "04_archetype.txt")
    attribute_path = os.path.join(results_path, "04_attribute.txt")
    scenario_questions_path = os.path.join(results_path, "04_scenario_questions.txt")
    scenario_choices_path = os.path.join(results_path, "04_scenario_choices.txt")

    # setup_archetype_attribute_scenario(
    #     eabss_components_path,
    #     archetype_path,
    #     attribute_path,
    #     scenario_questions_path,
    #     scenario_choices_path,
    # )

    scenario_ground_truth_path = os.path.join(
        results_path, "04_scenario_ground_truth.txt"
    )
    create_ground_truth(scenario_questions_path, scenario_ground_truth_path)
