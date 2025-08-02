import re
from google.genai.types import GenerateContentResponse

import display_progress
from system_path import SystemPath
import llm
from models.response_models import Scenario


def design_profile_n_scenario(path: SystemPath):
    setup_profile_attribute(path)
    setup_archetype(path)
    setup_scenario(path)


def setup_profile_attribute(path: SystemPath):
    response = generate_potential_profile_attributes(path)

    print("-" * 50)
    print("Define profile attributes.")
    print("-" * 50)
    print()
    print("Suggestions:")
    for e in response.parsed:
        print(f"    - {e}")

    print(
        f"""
Example:
    Please enter the number of attributes: 2
    Enter Attribute 1 text: Age
    Enter Attribute 2 text: Occupation

{"-"*50}
"""
    )

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
{display_progress.eabss_scope_progress(path)}

Please suggest {3} potential {main_actor} attributes.

For example: Race, Age, Occupation
"""
    response = llm.generate_content(
        prompt,
        response_schema=list[str],
    )
    return response


def setup_archetype(path: SystemPath):
    with open(path.get_04_attributes_path()) as f:
        attributes = f.read().strip().splitlines()

    response = generate_potential_archetype(path, attributes)

    print("-" * 50)
    print("Define Agent Archetypes")
    print("-" * 50)
    print()
    print("Suggestions:")
    for e in response.parsed:
        print(f"    - {e}")

    print(
        f"""
Example:
    Please enter number of archetypes: 2
    Enter Archetype 1: Early bird
    Enter Archetype 2: Night owl

{"-"*50}
"""
    )

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
{display_progress.eabss_scope_progress(path)}

And attribute
{", ".join(attributes)}

Please suggest {3} potential {main_actor} archetypes.
For example: Early Bird, Night Owl, Mixed
"""
    response = llm.generate_content(
        prompt,
        response_schema=list[str],
    )
    return response


def setup_scenario(path: SystemPath):
    response = generate_potential_scenario(path)
    scenario: Scenario = response.parsed

    print("-" * 50)
    print("Define scenario questions and answers choices.")
    print(
        "For simplicity of the model, please use questions that can answer with the same set of choices."
    )
    print(
        """Example: 
    Choice 1: Stay at home
    Choice 2: Travel
    Choice 3: Go nearby restaurant

    Question 1: Which choice you would pick in normal situation?
    Question 2: Which choice you would pick when it rain?
    Question 3: Which choice you would pick when it is on weekend?"""
    )
    print("-" * 50)
    print()
    print("Choice Suggestions:")
    for choice in scenario.choices:
        print(f"    - {choice}")
    setup_scenario_choices(path)

    print("-" * 50)
    print()
    print("Question Suggestions:")
    for question in scenario.questions:
        print(f"    - {question}")
    setup_scenario_questions(path)

    print()


def generate_potential_scenario(path: SystemPath) -> GenerateContentResponse:

    prompt = f"""
Based on the scope
{display_progress.eabss_scope_progress(path)}

Please suggest {3} scenario answer choices and {3} scenario questions.
For simplicity of the model, please use questions that can answer with the same set of choices.

For example: 
Choice 1: Stay at home
Choice 2: Travel
Choice 3: Go nearby restaurant

Question 1: Which choice you would pick in normal situation?
Question 2: Which choice you would pick when it rain?
Question 3: Which choice you would pick when it is on weekend?
"""
    response = llm.generate_content(
        prompt,
        response_schema=Scenario,
    )
    return response


def setup_scenario_choices(path: SystemPath):

    print(
        f"""
Scenario Choices Example:
    Please enter number of answer choices: 3
    Enter Choice 1: Walking
    Enter Choice 2: Cycling
    Enter Choice 3: Driving

{"-"*50}
"""
    )

    while True:
        try:
            answer_size = int(input("Please enter number of answer choices: ").strip())
            break
        except:
            pass

    answers = []
    for i in range(answer_size):
        while True:
            answers_text = input(f"Enter Choice {i+1}: ")
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
Scenario Questions Example:
    Please enter number of questions: 2
    Enter Question 1 text: Which choice you would pick in normal situation?
    Enter Question 2 text: Which choice you would pick when it rain?

{"-"*50}
"""
    )
    while True:
        try:
            questions_size = int(input("Please enter number of questions: "))
            break
        except:
            pass

    questions = []
    for i in range(questions_size):
        while True:
            questions_text = input(f"Enter Question {i+1} text: ")
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
    print(f"Scenario questions saved to: '{path.get_04_scenario_questions_path()}'")


if __name__ == "__main__":
    path = SystemPath("results_travel_1")
    design_profile_n_scenario(path)
