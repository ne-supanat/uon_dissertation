import os
from dotenv import load_dotenv
from google import genai

import prompt


def extractProfile(prompt: prompt.Prompt):
    # Extract profile
    prompt = prompt.buildPrompt()
    # print(prompt)

    return generateProfile(prompt)


def generateProfile(prompt):
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=GOOGLE_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    print(response.text)
    return response.text
