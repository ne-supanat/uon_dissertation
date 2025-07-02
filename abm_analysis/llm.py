import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentResponse, GenerateContentConfig


def generate_content(prompt: str, response_schema=None) -> GenerateContentResponse:
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=GOOGLE_API_KEY)

    config = GenerateContentConfig(
        temperature=0.0,  # the randomness of responses - default: 1
        top_p=0.9,  # the sum of candidate token probabilities - default: 0.5
    )

    if response_schema:
        config.response_mime_type = "application/json"
        config.response_schema = response_schema

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=config,
    )

    print(response.text)
    print(response.usage_metadata.total_token_count)
    return response


if __name__ == "__main__":
    response = generate_content("write a poem about cat and dog. only 4 lines")

#     interview = ""
#     with open("data/mvp_1.txt", "r") as f:
#         interview = f.read()

#     response = generate_content(
#         f"""
# base on this transcript
# {interview}

# extract key components for the simulation based on Engineering Agent-Based Social Simulations (EABSS) framework structure
# -	Actors (people/groups/organisation)
# -	Archetype (role/what they are allowed or expected to do)
# -	Social/Psychological aspect (rules or norms)
# -	key activities (behaviours performed under certain conditions)
# -	Physical component (tools or systems used)
# -	Interactions (who talks to or affects whom)
# -	Artificial lab (global variables)

# response in short and very simple way. this is just to outlite the model.
# """
#     )

#     print(response.usage_metadata.total_token_count)

# response = generateContent(
#         f"""
# base on this interview
# {interview}

# extract components for Modelling Agent systems based on Institutional Analysis (MAIA)
# -	Actors (people/groups)
# -	Roles (what they are allowed or expected to do)
# -	Institutions (rules or norms)
# -	Actions (behaviours performed under certain conditions)
# -	Artifacts (tools or systems used)
# -	Interactions (who talks to or affects whom)

# response in short and very simple way. this is just to outlite the model.
# """
#     )

#     response = generateContent(
#         f"""
# base on this interview
# {interview}

# list activity mention in the interview

# response in this format
# action:
# condition:
# evidence:

# for example
# interview:
# "every saturday, I go to park"

# response:
# action: "go to park"
# condition: "on saturday"
# evidence: "every saturday, I go to park"
# """
#     )
