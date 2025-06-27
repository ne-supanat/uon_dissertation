import json

import llm
from response_models import TransportationMode


# Create set of scenario questions
# easier to be done by human (only questions that matter to the system)
# def generate_scenario_questions():
#     prompt = f"""
# Generate set of {6} scenario-questions that let responders decide what to choose
# in different situation that needs to consider following options: Weather, Personal Health, Perceive Convenience, Environmental Impact, Cost
# with these transportation choices: Tram, Cycling, Taking Bus, Driving

# Response with only questions
# """
#     response = llm.generate_content(prompt, list[str])
#     return response.text


def _answer_scenario_questions(profile, questions) -> list[TransportationMode]:
    prompt = f"""
Based on this profile

{profile}

Answer these questions

{questions}
"""
    response = llm.generate_content(prompt, list[TransportationMode])
    result: list[TransportationMode] = response.parsed
    return result


def generate_profile_answers(question_path, profiles_path, answer_path):
    with open(question_path, "r") as f:
        questions = json.loads(f.read())
    with open(profiles_path, "r") as f:
        content = f.read()
    profiles = [p for p in content.split("\n\n") if p != ""]

    with open(answer_path, "a+") as f:
        for profileStr in profiles:
            profile: dict = json.loads(profileStr)
            answers = _answer_scenario_questions(profile, questions)
            f.write(f"{profile['file']};{profile['archetype']};")
            f.write(";".join(answers))
            f.write("\n")


if __name__ == "__main__":
    generate_profile_answers(
        "mvp/results/scenario_questions.txt",
        "mvp/results/profiles.txt",
        "mvp/results/scenario_answer_record.csv",
    )
