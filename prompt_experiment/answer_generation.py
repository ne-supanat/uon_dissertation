from typing import Literal
import json
import random

import mvp.llm as llm


def answer(
    profile: str, questionType: Literal["label", "score"], questions: list[dict | str]
) -> list[str] | list[float]:
    answers = []
    if questionType == "label":
        for question in questions:
            answers.append(answerLabelQuestion(profile, question))
    else:
        for question in questions:
            answers.append(answerScoreQeustion(profile, question))

    return answers


def answerLabelQuestion(profile: str, questionDict: dict):
    question: str = questionDict["question"]
    choices: list[str] = questionDict["choices"]

    prompt = f"""Using this profile
{profile}

Answer this question:
{question}

Pick from this choices:
{', '.join(random.shuffle(choices))}

Please respone with only the answer(s). For example:
if answer is {choices[0]} the response is {choices[0]}
if answer are {choices[0]} and {choices[1]} the response are {choices[0]};{choices[1]}
"""

    response = llm.generate_content(prompt)
    responseText = response.text.strip()
    responseItems = [item.strip() for item in responseText.split(";")]

    print(f"answer label: {response.usage_metadata.total_token_count}")

    return responseItems


def answerScoreQeustion(profile: str, question: str):
    prompt = f"""Using this profile
{profile}

Please rate the following statement:
{question}

Please respone with only the score where 
1 means Striongly disagree
2 means Disagree
3 means Neutral
4 means Agree
5 means Strongly agree

For example:
if the answer is Agree, the response is 4
"""

    response = llm.generate_content(prompt)
    responseText = response.text.strip()
    print(f"answer score: {response.usage_metadata.total_token_count}")
    return float(responseText)
