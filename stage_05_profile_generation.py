import os
import json
from google.genai.types import GenerateContentResponse

import llm
from models.response_models import Profile
import display_progress


def generate(
    document_paths: list[str],
    objective_statement_path: str,
    eabss_components_path: str,
    attribute_path: str,
    profiles_path: str,
):
    with open(objective_statement_path, "r") as f:
        objective_statement = f.read()
        objective_statement: dict = json.loads(objective_statement)
        objective = objective_statement["objective"]

    with open(attribute_path, "r") as f:
        profile_attributes = f.read().splitlines()

    # New file
    with open(profiles_path, "w") as f:
        f.write("")

    for document_path in document_paths:
        document = ""
        with open(document_path, "r") as f:
            document = f.read()
        response = extract_profile(
            document,
            profile_attributes,
            objective,
            eabss_components_path,
            document_path,
        )

        with open(profiles_path, "a+") as f:
            f.write(response.text)
            f.write("\n\n")


def extract_profile(
    document: str,
    profile_attributes: list[str],
    objective: str,
    eabss_scope_path: str,
    document_path: str,
) -> GenerateContentResponse:
    prompt = f"""
Base on this transcript

{document}

And EABSS component
{display_progress.eabss_components_progress(eabss_scope_path)}

Summarise profile within 100 words that related to objective: {objective}
Find supporting evidence (quotes) that related to objective and key components

Using information from profile summary and quotes, 
Identify attributes of this profile.
{"\n".join([f'{i+1}. {attr}' for i,attr in enumerate(profile_attributes)])}

Using information from profile summary and quotes, 
Classify this profile archetype from archetype in EABSS component

file is {document_path}
"""
    response = llm.generate_content(prompt, Profile)
    return response


if __name__ == "__main__":
    document_paths = ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    results_path = "results_3"
    objective_statement_path = os.path.join(results_path, "01_objective.txt")
    eabss_components_path = os.path.join(results_path, "02_eabss_scope.txt")
    attribute_path = os.path.join(results_path, "04_attribute.txt")
    profiles_path = os.path.join(results_path, "05_profiles.txt")

    generate(
        document_paths,
        objective_statement_path,
        eabss_components_path,
        attribute_path,
        profiles_path,
    )
