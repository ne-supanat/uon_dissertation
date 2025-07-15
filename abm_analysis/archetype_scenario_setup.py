import json


def setup_archetype_scenario(
    eabss_components_path,
    archetype_path,
    scenario_questions_path,
    scenario_choices_path,
):
    setup_archetype(eabss_components_path, archetype_path)
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
    # TODO: change path to models/archetype.py
    model_archetype_path = "abm_analysis/models/archetypes.py"

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


def setup_scenario(questions_path, scenario_choices_path):
    print("\nDefine scenario questions and answers choices.")
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
    # TODO: change path to models/scenario_choices.py
    answer_choices_path = "abm_analysis/models/scenario_choices.py"

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
    results_path = "abm_analysis/results_1"
    eabss_components_path = results_path + "/eabss_scope.txt"
    archetype_path = results_path + "/archetypes.txt"
    scenario_questions_path = results_path + "/scenario_questions.txt"
    scenario_choices_path = results_path + "/scenario_choices.txt"
    setup_archetype_scenario(
        eabss_components_path,
        archetype_path,
        scenario_questions_path,
        scenario_choices_path,
    )
