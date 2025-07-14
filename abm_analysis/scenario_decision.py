import json

import llm
from response_models import Profile
from models.scenario_answer_choices import ScenarioChoice


def _answer_scenario_questions(profile, questions) -> list[ScenarioChoice]:
    prompt = f"""
Based on this profile

{profile}

Answer these questions

{questions}
"""
    response = llm.generate_content(prompt, list[ScenarioChoice])
    result: list[ScenarioChoice] = response.parsed
    return result


def generate_profile_answers(question_path, profiles_path, answer_path):
    with open(question_path, "r") as f:
        questions = json.loads(f.read())
    with open(profiles_path, "r") as f:
        content = f.read()
    profiles = [profile for profile in content.strip().split("\n\n")]

    # TODO: hide archetype

    with open(answer_path, "a+") as f:
        for profileStr in profiles:
            profile: Profile = Profile.model_validate_json(profileStr)
            answers = _answer_scenario_questions(profile.model_dump_json(), questions)
            f.write(f"{profile.file};{profile.archetype.value};")
            f.write(";".join([a.value for a in answers]))
            f.write("\n")


if __name__ == "__main__":
    scenario_questions_path = "abm_analysis/results/scenario_questions.txt"
    profiles_path = "abm_analysis/results/profiles.txt"
    scenario_answers_path = "abm_analysis/results/scenario_answers.csv"

    generate_profile_answers(
        scenario_questions_path,
        profiles_path,
        scenario_answers_path,
    )
