import json
import llm
from response_models import Profile


def extract_profile(
    interview: str,
    profile_attrs: list[str],
    objective: str,
    key_components: str,
):
    prompt = f"""
Base on this interview.

{interview}

and Key components

{key_components}

{f"""1. Extract following profile data:\n{[f"- {attr}\n" for attr in profile_attrs]}""" if profile_attrs else ""}
2. Find supporting evidence (quotes) that related to {objective}
3. Identify archetype base on archetype in key component
"""
    response = llm.generate_content(prompt, Profile)
    return response.text


def generate_profile():
    objective = ""

    with open("mvp/results/key_components.txt", "r") as f:
        key_components = f.read()

    # profiles
    for i in range(1, 4):
        interview = ""
        file_name = f"data/mvp_{i}.txt"
        with open(file_name, "r") as f:
            interview = f.read()
        profileStr = extract_profile(
            interview, ["age", "distance from homw to work"], objective, key_components
        )

        profile: dict = json.loads(profileStr)
        profile["file"] = file_name

        with open(f"mvp/results/profiles.txt", "a+") as f:
            f.write(json.dumps(profile))
            f.write("\n\n")
