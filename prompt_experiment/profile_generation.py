import os
from dotenv import load_dotenv
from google import genai

import prompt_experiment.prompt as prompt
import mvp.llm as llm


def generateProfile(prompt: prompt.Prompt):
    buildProfilePrompt = prompt.buildProfilePrompt()
    response = llm.generate_content(buildProfilePrompt)
    profile = response.text
    # print(profile)

    print(f"profile: {response.usage_metadata.total_token_count}")

    if profile.startswith("```json"):
        profile = profile.replace("```json\n{", "").replace("}\n```", "")

    #     profile = """
    # "name": "None",
    # "age": "32",
    # "occupation": "Marine Biologist (recently graduated)",
    # "key_memory": [
    # "i traveled for eight months in central america",
    # "diving the blue whole in belize it was really amazing"
    # ],
    # "domain_label": "fav_warm",
    # "domain_label_reason": "The participant traveled to Central America for eight months and mentions diving in Belize, both of which are tropical or warm locations. This suggests a preference for warm climates and destinations."
    # """

    profile = "{" + profile.replace("\n", "") + "}"

    return profile
