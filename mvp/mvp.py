import os
import enum
import json
import pandas as pd
from pydantic import BaseModel

import llm

import thematic_analysis as ta
import thematic_analysis_evaluation as tae
import key_component_generation as kcg

import profile_generation as pg
import profile_generation_evaluation as pge
import scenario_decision as sd
import scenario_decision_evaluation as sde
import decision_table as dt


def get_objective():
    return "explore sustainability in different usages of transportation from home to workplace"


def get_input_output():
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


def generate_simulation_script(
    obj, input, output, key_component, usecase, activity, state_transition, action_prob
):
    prompt = f"""
Based on these EABSS key components

{key_component}

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
{state_transition}

Archetype action probability
{action_prob}

generate agentPy simulation script
"""
    response = llm.generate_content(prompt)
    return response.text


def main():
    os.makedirs("mvp/results", exist_ok=True)

    # objective
    objective = "explore different usages of transportation from home to workplace"

    # input, output
    input, output = get_input_output()

    document_paths = ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]

    ta_codes_txt_path = "mvp/results/thematic_analysis_codes.txt"
    ta_codes_csv_path = "mvp/results/thematic_analysis_codes.csv"

    # Extract key components codes with supporting quotes
    ta.thematic_analyse(document_paths, ta_codes_txt_path, ta_codes_csv_path)
    tae.evaluate(document_paths)

    # Generate ABM key components
    kcg.generate()
    # + human review: codes and quotes coherence

    # Profiles generation
    pg.generate_profile()
    pge.evaluate_profile()
    # + human review: attribute correctness and archetype and quotes coherence

    # # Scenario-question answering
    # sd.generate_profile_answers(
    #     "mvp/results/scenario_questions.txt",
    #     "mvp/results/profiles.txt",
    #     "mvp/results/scenario_answer_record.csv",
    # )
    # sde.score_anwser()

    # # Decision table
    # dt.generate()

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


if __name__ == "__main__":
    main()
