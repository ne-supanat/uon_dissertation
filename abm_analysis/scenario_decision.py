import random

import llm
from response_models import Profile, ProfileShort
from models.archetypes import Archetype
from models.scenario_choices import ScenarioChoice


def generate_profile_scenario_answers(question_path, profiles_path, answer_path):
    with open(question_path, "r") as f:
        questions = f.read().strip().split("\n")

    with open(profiles_path, "r") as f:
        content = f.read()
    profiles = [profile for profile in content.strip().split("\n\n")]

    # TODO: hide archetype

    # New file
    with open(answer_path, "w") as f:
        f.write()

    with open(answer_path, "a+") as f:
        for profile_str in profiles:
            profile: ProfileShort = ProfileShort.model_validate_json(profile_str)
            answers = answer_scenario_questions(profile, questions)
            f.write(f"{profile.file};{profile.archetype.value};")
            f.write(";".join([a.value for a in answers]))
            f.write("\n")


def answer_scenario_questions(
    profile: ProfileShort,
    questions: list[str],
) -> list[ScenarioChoice]:
    prompt = f"""
Based on this profile

{profile}

Answer these questions

{questions}
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
    scenario_questions_path = "abm_analysis/results_2/scenario_questions.txt"
    profiles_path = "abm_analysis/results/profiles.txt"
    scenario_answers_path = "abm_analysis/results_2/profile_scenario_answers.csv"

    # generate_profile_answers(
    #     scenario_questions_path,
    #     profiles_path,
    #     scenario_answers_path,
    # )

    mock_scenario_answer(scenario_questions_path, scenario_answers_path)
