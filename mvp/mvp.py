import os
import enum
import json
import pandas as pd
from pydantic import BaseModel

import llm


# TODO: function, variable name format


class InputOutput(BaseModel):
    input: str
    output: str


class Archetype(enum.Enum):
    PragmaticCommuter = "Pragmatic Commuter"
    EnvironmentallyAwareCommuter = "Environmentally Aware Commuter"


class Profile(BaseModel):
    attrs: list[str]
    quotes: list[str]
    archetype: Archetype


class TransportationMode(enum.Enum):
    Tram = "Tram"
    Cycling = "Cycling"
    Bus = "Bus"
    Driving = "Driving"


def getObjective():
    return "explore sustainability in different usages of transportation from home to workplace"


def getInputOutput():
    # response = llm.generateContent(
    #     prompt=f"""based on this objective: {obj}, what should be input and output of the simulation to satisfied the objective""",
    #     response_schema=InputOutput,
    # )

    # # Use instantiated objects.
    # inputOutput: InputOutput = response.parsed

    # print(inputOutput)
    # return inputOutput.input, inputOutput.output

    # return input, output
    return (
        "traveller characteristic (age, gender, occupation, transportation preference)",
        "number of used of each transportation type",
    )


def extract_code_and_quote(interview: str) -> str:
    prompt = f"""
Based on this transcript

{interview}

Use Engineering Agent-Based Social Simulations (EABSS) framework structure
-	Actors (people/groups/organisation)
-	Archetype (role/what they are allowed or expected to do)
-	Social/Psychological aspect (rules or norms)
-	Key activities (behaviours performed under certain conditions)
-	Physical component (tools or systems used)
-	Interactions (who talks to or affects whom)

Perform thematic analysis on it. Focus only participant responses.
follow these steps
1. read the transcript
2. identify components and supporting quotes under EABSS key components

Please reponse in this format
key component 1
- "code 1"
    - "supporting quote 1"
    - "supporting quote 2"
- "code 2"
    - "supporting quote 1"
    - "supporting quote 2"
"""
    response = llm.generateContent(prompt)
    return response.text


def finalise_codes_quotes(
    codesQuotes: str,
    objective: str,
    input: str,
    output: str,
) -> str:
    prompt = f"""
Based on following codes and quotes

{codesQuotes}

Use Engineering Agent-Based Social Simulations (EABSS) framework structure
-	Actors (people/groups/organisation)
-	Archetype (role/what they are allowed or expected to do)
-	Social/Psychological aspect (rules or norms)
-	key activities (behaviours performed under certain conditions)
-	Physical component (tools or systems used)
-	Interactions (who talks to or affects whom)

Select minimum items from each each components that are the most important to build Agent-based modeling simulation with
objective: {objective}
input: {input}
output: {output}

Please reponse in this format
key component 1
- "code 1"
    - "supporting quote 1"
    - "supporting quote 2"
- "code 2"
    - "supporting quote 1"
    - "supporting quote 2"
"""
    response = llm.generateContent(prompt)
    return response.text


def drawUsecaseDiagram(keyComponent: str):
    prompt = f"""
Based on following Engineering Agent-Based Social Simulations (EABSS) key components

{keyComponent}

generate UML use case diagram for all key activities
response in plantUML format
"""
    response = llm.generateContent(prompt)
    return response.text


def drawActivityDiagram(keyComponent: str):
    prompt = f"""
Based on following Engineering Agent-Based Social Simulations (EABSS) key components

{keyComponent}

generate UML activity diagram for all key activities
response in plantUML format
"""
    response = llm.generateContent(prompt)
    return response.text


def drawStateTransitionDiagram(keyComponent: str):
    prompt = f"""
Based on following Engineering Agent-Based Social Simulations (EABSS) key components

{keyComponent}

generate UML state transition diagram of actor acretype if needed
response in plantUML format
"""
    response = llm.generateContent(prompt)
    return response.text


def extract_profile(
    interview: str,
    profileAttrs: list[str],
    objective: str,
    keyComponents: str,
):
    prompt = f"""
Base on this interview.

{interview}

and Key components

{keyComponents}

{f"""1. Extract following profile data:\n{[f"- {attr}\n" for attr in profileAttrs]}""" if profileAttrs else ""}
2. Find supporting evidence (quotes) that related to {objective}
3. Identify archetype base on archetype in key component
"""
    response = llm.generateContent(prompt, Profile)
    return response.text


def generateScenarioQuestions():
    prompt = f"""
Generate set of {6} scenario-questions that let responders decide what to choose
in different situation that needs to consider following options: Weather, Personal Health, Perceive Convenience, Environmental Impact, Cost
with these transportation choices: Tram, Cycling, Taking Bus, Driving

Response with only questions
"""
    response = llm.generateContent(prompt, list[str])
    return response.text


def answerQuestions(profile, questions):
    prompt = f"""
Based on this profile

{profile}

answer this question

{questions}
"""
    response = llm.generateContent(prompt, list[TransportationMode])
    return response.text


def generateSimulationScript(
    obj, input, output, keyComponent, usecase, activity, stateTransition, actionProb
):
    prompt = f"""
Based on these EABSS key components

{keyComponent}

Objective
{obj}

Input
{input}

Output
{output}

UML use case diagram
{usecase}

UML activity diagram
{activity}

UML state transition diagram
{stateTransition}

Archetype action probability
{actionProb}

generate agentPy simulation script
"""
    response = llm.generateContent(prompt)
    return response.text


def main():
    os.makedirs("mvp/results", exist_ok=True)

    # objective
    obj = "explore different usages of transportation from home to workplace"

    # input, output
    input, output = getInputOutput()

    # # codes, quotes
    # for i in range(1,4):
    #     interview = ""
    #     file_name = f"data/mvp_{i}.txt"
    #     with open(file_name, "r") as f:
    #         interview = f.read()
    #     codesAndQuotes = extract_code_and_quote(interview)

    #     # save codes, quotes
    #     with open(f"mvp/results/codes_quotes.txt", "a+") as f:
    #         f.write(f"{file_name}\n")
    #         f.write(codesAndQuotes)
    #         f.write("\n\n")

    # # finalise EABSS key components
    # with open("mvp/results/codes_quotes.txt", "r") as f:
    #     codesQuotes = f.read()
    # keyComponents = finalise_codes_quotes(codesQuotes, obj, input, output)

    # # save key component
    # with open(f"mvp/results/key_components.txt", "w") as f:
    #     f.write(keyComponents)

    with open("mvp/results/key_components.txt", "r") as f:
        keyComponents = f.read()

    # # key activities - UML use case diagram
    # usecaseDiagram = drawKeyActivityUsecaseDiagram(keyComponents)
    # with open(f"mvp/results/usecase_diagram.txt", "w") as f:
    #     f.write(usecaseDiagram)

    # activityDiagram = drawActivityDiagram(keyComponents)
    # with open(f"mvp/results/activity_diagram.txt", "w") as f:
    #     f.write(activityDiagram)

    # # user state machine - UML state diagram
    # stateTransitionDiagram = drawStateTransition(keyComponents)
    # with open(f"mvp/results/state_transition_diagram.txt", "w") as f:
    #     f.write(stateTransitionDiagram)

    # # profiles
    # for i in range(1, 4):
    #     interview = ""
    #     file_name = f"data/mvp_{i}.txt"
    #     with open(file_name, "r") as f:
    #         interview = f.read()
    #     profileStr = extract_profile(
    #         interview, ["age", "distance from homw to work"], obj, keyComponents
    #     )

    #     profile: dict = json.loads(profileStr)
    #     profile["file"] = file_name

    #     with open(f"mvp/results/profiles.txt", "a+") as f:
    #         f.write(json.dumps(profile))
    #         f.write("\n\n")

    # # generate scenario-questions
    # questions = generateScenarioQuestions()
    # with open(f"mvp/results/scenario_questions.txt", "a+") as f:
    #     f.write(questions)

    # scenario-question answering
    with open(f"mvp/results/scenario_questions.txt", "r") as f:
        questions = json.loads(f.read())
    with open("mvp/results/profiles.txt", "r") as f:
        content = f.read()
        profiles = [p for p in content.split("\n\n") if p != ""]

    # with open(f"mvp/results/answer_record.csv", "a+") as f:
    #     for profileStr in profiles:
    #         profile: dict = json.loads(profileStr)
    #         answers = answerQuestions(profile, questions)
    #         f.write(f"{profile['file']};{profile['archetype']};")
    #         f.write(";".join(json.loads(answers)))
    #         f.write("\n")

    # # action decision table
    # df = pd.read_csv("mvp/results/answer_record.csv", sep=";", header=None)
    # df.columns = ["file", "type"] + [f"q{i+1}" for i in range(len(questions))]

    # with open(f"mvp/results/answer_prob.csv", "a+") as f:
    #     for type in Archetype:
    #         archetypeDF = df[df["type"] == type.value]
    #         archetypeSize = archetypeDF.shape[0]

    #         for i in range(len(questions)):
    #             for mode in TransportationMode:
    #                 answerDF = archetypeDF[archetypeDF[f"q{i+1}"] == mode.value]

    #                 prob = answerDF.shape[0] / archetypeSize
    #                 print(f"{type.value};{questions[i]};{mode.value};{prob}")

    #                 f.write(f"{type.value};{questions[i]};{mode.value};{prob}\n")

    # # gen simulation script
    # with open(f"mvp/results/usecase_diagram.txt", "r") as f:
    #     usecase = f.read()

    # with open(f"mvp/results/activity_diagram.txt", "r") as f:
    #     activity = f.read()

    # with open(f"mvp/results/state_transition_diagram.txt", "r") as f:
    #     stateTransition = f.read()

    # with open(f"mvp/results/answer_prob.csv", "r") as f:
    #     actionProb = f.read()

    # script = generateSimulationScript(
    #     obj,
    #     input,
    #     output,
    #     keyComponents,
    #     usecase,
    #     activity,
    #     stateTransition,
    #     actionProb,
    # )
    # with open(f"mvp/results/script.py", "w") as f:
    #     f.write(script)

    # evaluation
    #


if __name__ == "__main__":
    main()
