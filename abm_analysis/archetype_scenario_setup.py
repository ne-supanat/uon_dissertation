import json


def setup_archetype_scenario(
    eabss_components_path,
    archetype_path,
    questions_path,
    answer_choices_path,
):
    setup_archetype(eabss_components_path, archetype_path)
    setup_scenario(questions_path, answer_choices_path)


def setup_archetype(
    eabss_components_path,
    archetype_path,
):
    print("\nDefine Archetypes.")
    with open(eabss_components_path, "r") as f:
        scope_raw = f.read()
        scope: dict = json.loads(scope_raw)

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

    with open(archetype_path, "w") as f:
        f.write(content)

    print(f"\nArchetype result saved to: '{archetype_path}'")


def setup_scenario(questions_path, answer_choices_path):
    print("\nDefine scenario questions and answers choices.")
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
    setup_scenario_answer_choices(answer_choices_path)


def setup_scenario_questions(questions_path):
    while True:
        try:
            questions_size = int(input("Please enter the number of questions: "))
            break
        except:
            pass

    questions = []
    for i in range(questions_size):
        questions_text = input(f"Enter the question {i+1} text: ")
        questions.append(questions_text)

    # Example output
    # ----------------
    # [
    # What is your transport mode in usual days?,
    # What is your transport mode when it raining?
    # ]

    with open(questions_path, "w") as f:
        f.write(f'[\n{',\n'.join(questions)}\n]')

    print(f"\nScenario-questions result saved to: '{questions_path}'")


def setup_scenario_answer_choices(answer_choices_path):
    while True:
        try:
            answer_size = int(input("Please enter the number of answer choices: "))
            break
        except:
            pass

    answers = []
    for i in range(answer_size):
        answers_text = input(f"Choice {i+1}: ")
        answers.append(answers_text)

    # Example output
    # ----------------
    #

    content = "import enum\n\nclass ScenarioChoice(enum.Enum):\n"
    for item in answers:
        content += f"""\t{"".join([word.lower().capitalize() for word in item.split(" ")])} = "{item}"\n"""

    with open(answer_choices_path, "w") as f:
        f.write(content)

    print(f"\nScenarion-answer choices result saved to: '{answer_choices_path}'")


if __name__ == "__main__":
    results_path = "abm_analysis/results_1"
    eabss_components_path = results_path + "/eabss_scope.txt"
    archetype_path = results_path + "/archetype.py"
    questions_path = results_path + "/questions.txt"
    answer_choices_path = results_path + "/answer_choices.py"

    setup_archetype_scenario(
        eabss_components_path, archetype_path, questions_path, answer_choices_path
    )
