import random
import csv

import llm
from models.response_models import Profile
from models.archetypes import Archetype
from models.scenario_choices import ScenarioChoice

from system_path import SystemPath


def create_profile_scenario_answers(path: SystemPath):
    with open(path.get_04_scenario_questions_path(), "r") as f:
        questions = f.read().strip().splitlines()

    with open(path.get_05_profiles_path(), "r") as f:
        content = f.read()
    profiles = [profile for profile in content.strip().split("\n\n")]

    with open(path.get_06_profile_scenario_answers_path(), "w") as f:
        for profile_str in profiles:
            profile: Profile = Profile.model_validate_json(profile_str)
            answers = generate_profile_scenario_answers(profile, questions)
            f.write(f"{profile.file};{profile.archetype.value};")
            f.write(";".join([a.value for a in answers]))
            f.write("\n")


def generate_profile_scenario_answers(
    profile: Profile,
    questions: list[str],
) -> list[ScenarioChoice]:
    prompt = f"""
Based on this profile summary:
{profile.summary}

Profile attributes:
{"\n".join([f'{i+1}. {attribute}' for i,attribute in enumerate(profile.attributes)])}

Supporting quotes:
{"\n".join([f'{i+1}. {quote}' for i,quote in enumerate(profile.quotes)])}

Answer following questions:
{"\n".join([f'{i+1}. {question}' for i,question in enumerate(questions)])}
"""
    response = llm.generate_content(prompt, list[ScenarioChoice])
    result: list[ScenarioChoice] = response.parsed
    return result


def mock_profile_scenario_answer(path: SystemPath):
    with open(path.get_04_scenario_questions_path(), "r") as f:
        questions = f.read().strip().splitlines()

    with open(path.get_06_profile_scenario_answers_path(), "w") as f:
        for i in range(100):
            archetype = random.choice([archetype.value for archetype in Archetype])
            answers = [
                random.choices(
                    [choice._value_ for choice in ScenarioChoice],
                    weights=(
                        [1, 9]
                        if archetype == [a.value for a in Archetype][0]
                        else [9, 1]
                    ),
                    k=1,
                )[0]
                for _ in range(len(questions))
            ]
            f.write(f"{i};{archetype};" + ";".join(answers) + "\n")
    print("saved at " + path.get_06_profile_scenario_answers_path())


def create_decision_probability_table(path: SystemPath):
    # Fetch scenario questions
    with open(path.get_04_scenario_questions_path(), "r") as f:
        questions = f.read().strip().splitlines()

    # Initialize answer and archetype counters
    answer_dict = {
        question: {
            archetype.value: {choice.value: 0 for choice in ScenarioChoice}
            for archetype in Archetype
        }
        for question in questions
    }
    archetype_counts = {archetype.value: 0 for archetype in Archetype}

    # Read scenario answers
    with open(path.get_06_profile_scenario_answers_path(), newline="") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            if not row or len(row) < 2 + len(questions):
                continue  # skip malformed rows
            archetype = row[1]
            archetype_counts[archetype] += 1
            for i, question in enumerate(questions):
                choice = row[2 + i]  # skip first 2 columns of filename and archetype
                answer_dict[question][archetype][choice] += 1

    # Write probabilities to output file
    with open(path.get_06_decision_probability_path(), "w") as f:
        for question in questions:
            for archetype in Archetype:
                count = archetype_counts[archetype.value]
                probs = [
                    (
                        answer_dict[question][archetype.value][choice.value] / count
                        if count > 0
                        else 0
                    )
                    for choice in ScenarioChoice
                ]

                line = (
                    f"{question};{archetype.value};"
                    + ";".join(f"{p:.2f}" for p in probs)
                    + "\n"
                )
                f.write(line)

    print()
    print("-" * 50)
    print(
        f"Decision probability table saved to: '{path.get_06_decision_probability_path()}'\n"
    )


if __name__ == "__main__":
    path = SystemPath("travel")

    # create_profile_scenario_answers(path)
    # create_decision_probability_table(path)

    # # NOTE: this is only for testing & development purpose
    mock_profile_scenario_answer(path)
    create_decision_probability_table(path)
