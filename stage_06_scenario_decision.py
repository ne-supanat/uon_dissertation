import os
import random

import llm
from models.response_models import Profile
from models.archetypes import Archetype
from models.scenario_choices import ScenarioChoice


def generate_profile_scenario_answers(question_path, profiles_path, answer_path):
    with open(question_path, "r") as f:
        questions = f.read().strip().split("\n")

    with open(profiles_path, "r") as f:
        content = f.read()
    profiles = [profile for profile in content.strip().split("\n\n")]

    with open(answer_path, "w") as f:
        for profile_str in profiles:
            profile: Profile = Profile.model_validate_json(profile_str)
            answers = answer_scenario_questions(profile, questions)
            f.write(f"{profile.file};{profile.archetype.value};")
            f.write(";".join([a.value for a in answers]))
            f.write("\n")


def answer_scenario_questions(
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


def mock_scenario_answer(question_path, answer_path):
    with open(question_path, "r") as f:
        questions = f.read().strip().split("\n")

    with open(answer_path, "w") as f:
        for i in range(100):
            archetype = random.choice([archetype.value for archetype in Archetype])
            answers = [
                random.choices(
                    [choice._value_ for choice in ScenarioChoice],
                    weights=(
                        [1, 1, 8]
                        if archetype == Archetype.PragmaticAdopter.value
                        else [4, 4, 2]
                    ),
                    k=1,
                )[0]
                for _ in range(len(questions))
            ]
            f.write(f"{i};{archetype};" + ";".join(answers) + "\n")
    print("saved at " + answer_path)


if __name__ == "__main__":
    results_path = "results_3"
    scenario_questions_path = os.path.join(results_path, "scenario_questions.txt")
    profiles_path = os.path.join(results_path, "profiles.txt")
    profile_scenario_answers_path = os.path.join(
        results_path, "profile_scenario_answers.csv"
    )

    generate_profile_scenario_answers(
        scenario_questions_path,
        profiles_path,
        profile_scenario_answers_path,
    )

    # # NOTE: this is only for testing & development purpose
    # mock_scenario_answer(scenario_questions_path, profile_scenario_answers_path)
