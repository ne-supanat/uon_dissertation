import json
import os

# TODO: (optional) sanitize name


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
        content += f"""\t{"".join([word.lower().capitalize() for word in item["code"].split(" ")])} = "{item["code"]}"\n"""

    with open(model_archetype_path, "w") as f:
        f.write(content)

    print(f"System's Archetype model updated at: '{model_archetype_path}'")


def setup_profile_attribute(attribute_path):
    print("-" * 50)
    print("Define profile attributes.")
    print(
        """
- Example input -
Please enter the number of attributes: 2

Enter the attribute 1 text: Age
Enter the attribute 2 text: Occupation
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

    print(f"\nProfile attributes saved to: '{attribute_path}'\n")


def setup_scenario(questions_path, scenario_choices_path):
    print("-" * 50)
    print("Define scenario questions and answers choices.")
    print(
        "For simplicity of the model, please use questions that can answer with the same set of choices."
    )
    print(
        """
- Example input -
Please enter the number of questions: 2

Enter the question 1 text: What is your transport mode in usual days?
Enter the question 2 text: What is your transport mode when it raining?

Enter number of answer choices: 3
Choice 1: Walking
Choice 2: Cycling
Choice 3: Driving
"""
    )
    setup_scenario_questions(questions_path)
    setup_scenario_choices(scenario_choices_path)
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

    print(f"\nScenario questions saved to: '{questions_path}'\n")


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

    print(f"Scenario choices saved at: '{scenario_choices_path}''")

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
        content += f"""\t{"".join([word.lower().capitalize() for word in item.split(" ")])} = "{item}"\n"""

    with open(answer_choices_path, "w") as f:
        f.write(content)

    print(f"\nSystem's Scenario choice model updated at: '{answer_choices_path}''")


if __name__ == "__main__":
    results_path = "results_3"

    eabss_components_path = os.path.join(results_path, "02_eabss_scope.txt")
    archetype_path = os.path.join(results_path, "04_archetype.txt")
    attribute_path = os.path.join(results_path, "04_attribute.txt")
    scenario_questions_path = os.path.join(results_path, "04_scenario_questions.txt")
    scenario_choices_path = os.path.join(results_path, "04_scenario_choices.txt")

    setup_archetype_attribute_scenario(
        eabss_components_path,
        archetype_path,
        attribute_path,
        scenario_questions_path,
        scenario_choices_path,
    )
