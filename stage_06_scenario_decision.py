import random
import csv

import llm
from models.response_models import Profile
from models.archetypes import Archetype
from models.scenario_choices import ScenarioChoice

from system_path import SystemPath

import json


def create_ground_truth(path: SystemPath):
    with open(path.get_04_scenario_questions_path(), "r") as f:
        content = f.read()
        scenario_questions = content.strip().splitlines()

    with open(path.get_06_scenario_ground_truth_path(), "w") as f:
        responses = []
        for scenario_question in scenario_questions:
            response = generate_ground_truth(scenario_question)
            responses.append(response.parsed)

        # Save ground truth
        # Example output
        # [
        #   {
        #     "qeustion": "question1?",
        #     "answer": {
        #         "archetype1": ["choice1", "choice2"],
        #         "archetype2": ["choice1", "choice2"],
        #         "archetype3": ["choice1", "choice2"],
        #     },
        #   },
        # ...
        # ]

        question_dict = []
        for i, question_block in enumerate(responses):
            q = {}
            q["question"] = scenario_questions[i]
            q["answer"] = {}

            for content, archetype in enumerate([a.value for a in Archetype]):
                q["answer"][archetype] = [c.value for c in question_block[content]]

            question_dict.append(q)

        content = json.dumps(question_dict, indent=4)
        f.write(content)

    print()
    print("-" * 50)
    print(
        f"Scenario ground truths saved to: '{path.get_06_scenario_ground_truth_path()}'\n"
    )


def generate_ground_truth(question: str):

    prompt = f"""
Archetypes are {", ".join([type.value for type in Archetype])}

For each archetype what are answers of the following question:
{question}

Choices are {", ".join([type.value for type in ScenarioChoice])}
answer can be in one, some, all or none of the choices

Respond in this format

{"{"}[
[choices archetype 1 would pick],
[choices archetype 2 would pick],
...
]{"}"}
"""

    response = llm.generate_content(prompt, list[list[ScenarioChoice]])
    return response


def create_profile_scenario_answer_from_ground_truth(path: SystemPath):
    with open(path.get_04_scenario_questions_path(), "r") as f:
        questions = f.read().strip().splitlines()

    with open(path.get_06_scenario_ground_truth_path(), "r") as f:
        content = f.read()
        ground_truth = json.loads(content)

    with open(path.get_06_profile_scenario_answers_path(), "w") as f:
        for i in range(100):
            archetype = random.choice([archetype.value for archetype in Archetype])

            answers = []
            for j in range(len(questions)):
                potential_answers = ground_truth[j]["answer"][archetype]
                answer = random.choice(potential_answers)
                answers.append(answer)

            f.write(f"{i};{archetype};" + ";".join(answers) + "\n")
    print("saved at " + path.get_06_profile_scenario_answers_path())


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

    # Create decision probability using ground truth (roleplay as archetype)
    # create_ground_truth(path)
    # mock_profile_scenario_answer_from_ground_truth(path)
    create_decision_probability_table(path)

    # Create decision probability using roleplay as profile
    # create_profile_scenario_answers(path)
    # create_decision_probability_table(path)
