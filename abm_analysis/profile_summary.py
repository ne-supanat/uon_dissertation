import json
from google.genai.types import GenerateContentResponse

import llm
from response_models import Profile


def summarise_profile(
    document: str,
) -> GenerateContentResponse:
    prompt = f"""
Base on this transcript

{document}

Summarise profile of participant
Respond in format of short description less than 100 words
"""
    response = llm.generate_content(prompt)
    return response


def generate(
    document_paths: list[str],
    profile_summary_path: str,
):
    for document_path in document_paths:
        document = ""
        with open(document_path, "r") as f:
            document = f.read()
        response = summarise_profile(
            document,
        )

        with open(profile_summary_path, "a+") as f:
            f.write(f"{document_path}\n")
            f.write(response.text)
            f.write("\n\n")


if __name__ == "__main__":
    document_paths = ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    profiles_path = "abm_analysis/results/profile_summary.txt"

    generate(
        document_paths,
        profiles_path,
    )
