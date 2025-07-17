import os
import json
from google.genai.types import GenerateContentResponse

import llm
from models.response_models import Profile, ProfileShort


def extract_profile(
    document: str,
    profile_attrs: list[str],
    objective: str,
    eabss_components: str,
    document_path: str,
) -> GenerateContentResponse:
    prompt = f"""
Base on this transcript

{document}

Summarise profile within 100 words that related to objective: {objective}
Find supporting evidence (quotes) that related to objective and key components
Using information from profile summary and quote, classify this profile archetype from archetype in key component

file is {document_path}
"""
    response = llm.generate_content(prompt, ProfileShort)

    return response


def generate(
    document_paths: list[str],
    objective_statement_path: str,
    eabss_components_path: str,
    profiles_path: str,
):
    with open(objective_statement_path, "r") as f:
        objective_statement = f.read()
        objective_statement: dict = json.loads(objective_statement)
        objective = objective_statement["objective"]

    with open(eabss_components_path, "r") as f:
        eabss_components = f.read()

    # New file
    with open(profiles_path, "w") as f:
        f.write("")

    for document_path in document_paths:
        document = ""
        with open(document_path, "r") as f:
            document = f.read()
        response = extract_profile(
            document,
            [
                "age: how old is participant",
                "distance: what is distance from homw to work",
            ],
            objective,
            eabss_components,
            document_path,
        )

        with open(profiles_path, "a+") as f:
            f.write(response.text)
            f.write("\n\n")


if __name__ == "__main__":
    document_paths = ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    results_path = "results_2"
    objective_statement_path = os.path.join(results_path, "objective.txt")
    eabss_components_path = os.path.join(results_path, "eabss_scope.txt")
    profiles_path = os.path.join(results_path, "profiles.txt")

    generate(
        document_paths,
        objective_statement_path,
        eabss_components_path,
        profiles_path,
    )
