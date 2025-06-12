import os
from dotenv import load_dotenv
from google import genai


def generateContent(prompt):
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=GOOGLE_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    print(response.text)
    return response.text
