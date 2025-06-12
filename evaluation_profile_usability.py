from typing import Literal
import json

import llm


def evaluateUsability(
    profile: str, questionType: Literal["label", "score"], questions: list[dict | str]
):
    jsonProfile = json.loads(profile)

    usability = []
    if questionType == "label":
        domainLabel = jsonProfile["domain_label"]
        for question in questions:
            usability.append(labelQuestion(profile, domainLabel, question))

        # mean accuracy
        usabilityScore = sum(usability) / len(usability)

        print(usability)
        print(f"Accuracy: {usabilityScore}")
    else:
        domainScore = float(jsonProfile["domain_score"])
        for question in questions:
            usability.append(scoreQeustion(profile, question))

        # error
        usabilityScore = abs(sum(usability) - domainScore)

        print(usability)
        print(f"Error: |{sum(usability)} - {domainScore}| = {usabilityScore}")

    return usabilityScore


def labelQuestion(profile: str, domainLabel: str, questionDict: dict):
    question: str = questionDict["question"]
    choices: list[str] = questionDict["choices"]
    choiceValues: list[str] = questionDict["choice_values"]

    jsonProfile = json.loads(profile)
    domainLabel = jsonProfile["domain_label"]

    prompt = f"""Using this profile
{profile}

Answer this question:
{question}

Pick from this choices:
{', '.join(choices)}

Please respone with only the answer(s). For example:
if answer is {choices[0]} the response is {choices[0]}
if answer are {choices[0]} and {choices[1]} the response are {choices[0]};{choices[1]}
"""

    response = llm.generateContent(prompt).strip()
    responseItems = [item.strip() for item in response.split(";")]

    score = 0.0
    for item in responseItems:
        if choiceValues[choices.index(item)] == domainLabel:
            score += 1

    return score / len(responseItems)  # accuracy percentage


def scoreQeustion(profile: str, question: str):
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

    response: str = llm.generateContent(prompt).strip()
    return float(response)
