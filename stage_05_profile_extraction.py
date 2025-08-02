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

And EABSS component
{display_progress.eabss_scope_progress(path)}

Summarise profile within 100 words that related to objective: {objective}
Find supporting evidence (quotes) that related to objective and key components

Using information from profile summary and quotes, 
Identify {1} answer from transcript for all {len(profile_attributes)} attribute of this profile.
Respond in this format
[
    "attribute1: answer",
    "attribute2: answer"
]

Using information from profile summary and quotes, 
Classify this profile archetype from archetype in EABSS component

file is {document_path}
"""
    response = llm.generate_content(prompt, Profile)
    return response


if __name__ == "__main__":
    path = SystemPath("results_4")
    document_paths = ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    extract_profile(path, document_paths)
