import json
import re

from system_path import SystemPath


def design_profile_n_scenario(path: SystemPath):
    setup_archetype(path)
    setup_profile_attribute(path)
    setup_scenario(path)


def setup_archetype(path: SystemPath):
    print("\nDefine Archetypes.")
    with open(path.get_02_eabss_scope_path(), "r") as f:
        scope_raw = f.read()
        scope: dict = json.loads(scope_raw)

    ## Save updated archetypes
    with open(path.get_04_archetypes_path(), "w") as f:
        f.write("\n".join(item["code"] for item in scope["archetypes"]))

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
    for item in scope["archetypes"]:
        content += f"""\t{"".join([word.lower().capitalize() for word in sanitise_name(item["code"]).split(" ")])} = "{item["code"]}"\n"""

    with open(model_archetype_path, "w") as f:
        f.write(content)

    print(f"System's Archetype model updated at: '{model_archetype_path}'")


def setup_profile_attribute(path: SystemPath):
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

    with open(path.get_04_attributes_path(), "w") as f:
        f.write(f'{'\n'.join(attributes)}')

    print()
    print("-" * 50)
    print(f"Profile attributes saved to: '{path.get_04_attributes_path()}'\n")


def setup_scenario(path: SystemPath):
    print("-" * 50)
    print("Define scenario questions and answers choices.")
    print(
        "For simplicity of the model, please use questions that can answer with the same set of choices."
    )
    setup_scenario_choices(path)
    setup_scenario_questions(path)
    print()


def setup_scenario_choices(path: SystemPath):

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
    with open(path.get_04_scenario_choices_path(), "w") as f:
        f.write("\n".join(answers))

    print()
    print("-" * 50)
    print(f"Scenario choices saved to: '{path.get_04_scenario_choices_path()}''")

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


def setup_scenario_questions(path: SystemPath):
    print(
        f"""
- Example input -
Please enter the number of questions: 2
Enter the question 1 text: What is your transport mode in usual days?
Enter the question 2 text: What is your transport mode when it raining?
{"-"*50}
"""
    )
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

    with open(path.get_04_scenario_questions_path(), "w") as f:
        f.write(f'{'\n'.join(questions)}')

    print()
    print("-" * 50)
    print(f"Scenario questions saved to: '{path.get_04_scenario_questions_path()}'\n")


if __name__ == "__main__":
    path = SystemPath("results_4")
    design_profile_n_scenario(path)
