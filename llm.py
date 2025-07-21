import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentResponse, GenerateContentConfig, Part

import requests

import display_progress
from models.response_models import ThinkResponse


def generate_content(prompt: str, response_schema=None) -> GenerateContentResponse:
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=GOOGLE_API_KEY)

    # Config parameter values
    # ref: https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/adjust-parameter-values
    config = GenerateContentConfig(
        temperature=0.0,  # the randomness of responses - default: 1
        top_p=0.0,  # the sum of candidate token probabilities - default: 0.5
        seed=0,  # fixed seed should provides the same response for same prompt - defualt: random number
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


def generate_content_from_images(
    image_paths: list[str], prompt: str, response_schema=None
):
    # Modification of Gemini's Image Understanding Documentation
    # ref: https://ai.google.dev/gemini-api/docs/image-understanding
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

    # Upload the first image
    for i in range(len(image_paths) - 1):
        uploaded_file = client.files.upload(file=image_paths[i])

    # Prepare the second image as inline data
    image2_path = image_paths[-1]
    with open(image2_path, "rb") as f:
        last_img_bytes = f.read()

    # Create the prompt with text and multiple images
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            prompt,
            uploaded_file,  # Use the uploaded file reference
            Part.from_bytes(data=last_img_bytes, mime_type="image/png"),
        ],
        config=config,
    )

    print(response.text)
    print(response.usage_metadata.total_token_count)
    return response


if __name__ == "__main__":
    # response = generate_content("write a poem about cat and dog. only 4 lines")
    results_path = "results_2"
    eabss_components_path = os.path.join(results_path, "eabss_scope.txt")

    prompt = f"""
Based on this EABSS components
{display_progress.eabss_components_progress(eabss_components_path)}

generate NetLogo simulation script
"""
    response = generate_content(prompt, ThinkResponse)
