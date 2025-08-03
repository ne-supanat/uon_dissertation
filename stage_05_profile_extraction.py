import json
from google.genai.types import GenerateContentResponse

import llm
from models.response_models import Profile
import display_progress

from system_path import SystemPath


def extract_profile(
    path: SystemPath,
    document_paths: list[str],
):
    with open(path.get_01_outline_path(), "r") as f:
        objective_statement = f.read()
        objective_statement: dict = json.loads(objective_statement)
        objective = objective_statement["objective"]

    with open(path.get_04_attributes_path(), "r") as f:
        profile_attributes = f.read().splitlines()

    # New file
    with open(path.get_05_profiles_path(), "w") as f:
        f.write("")

    for document_path in document_paths:
        document = ""
        with open(document_path, "r") as f:
            document = f.read()
        response = generate_profile(
            document,
            profile_attributes,
            objective,
            path,
            document_path,
        )

        with open(path.get_05_profiles_path(), "a+") as f:
            f.write(response.text)
            f.write("\n\n")

    print()
    print("-" * 50)
    print(f"Profiles result saved to: '{path.get_05_profiles_path()}'")


def generate_profile(
    document: str,
    profile_attributes: list[str],
    objective: str,
    path: SystemPath,
    document_path: str,
) -> GenerateContentResponse:
    prompt = f"""
Base on this transcript

{document}

Model's outline:
{display_progress.topic_outline_progress(path)}

Scenario detail:
{display_progress.scenario_progess(path)}

Summarise profile within 100 words that relevant to model's outline and scenario detail
Find supporting evidence (quotes) that related to model's outline and scenario detail

Using information from transcript to identify attributes:
{", ".join(profile_attributes)}

Identify an answer for each attribute in total of {len(profile_attributes)} attributes.
Respond in this format
[
    "attribute1: answer",
    "attribute2: answer"
]

Using information from profile summary and quotes, 
Classify this profile archetype

file is {document_path}
"""
    response = llm.generate_content(prompt, Profile)
    return response


if __name__ == "__main__":
    path = SystemPath("travel")
    document_paths = ["data/mvp/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"][:1]
    extract_profile(path, document_paths)
