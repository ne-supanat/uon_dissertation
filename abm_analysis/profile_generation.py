import json
from google.genai.types import GenerateContentResponse

import llm
from response_models import Profile


def extract_profile(
    document: str,
    profile_attrs: list[str],
    objective: str,
    key_component_scope: str,
    document_path: str,
) -> GenerateContentResponse:
    prompt = f"""
Base on this transcript

{document}

and this key components

{key_component_scope}

{f"""Extract following profile data:
 {[f"- {attr}\n" for attr in profile_attrs]}

reponse with only answer. for example "my age is 25" response with "25"
""" if profile_attrs else ""}

Find supporting evidence (quotes) that related to {objective}
Identify archetype base on archetype in key component

file is {document_path}
"""
    response = llm.generate_content(prompt, Profile)
    return response


def generate(
    document_paths: list[str],
    objective: str,
    key_component_scope_path: str,
    profiles_path: str,
):
    with open(key_component_scope_path, "r") as f:
        key_component_scope = f.read()

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
            key_component_scope,
            document_path,
        )

        with open(profiles_path, "a+") as f:
            f.write(response.text)
            f.write("\n\n")


if __name__ == "__main__":
    document_paths = ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    objective = "explore different usages of transportation from home to workplace"
    kc_scope_path = "abm_analysis/results/key_component_scope.txt"
    profiles_path = "abm_analysis/results/profiles.txt"

    generate(
        document_paths,
        objective,
        kc_scope_path,
        profiles_path,
    )
