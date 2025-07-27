import json
import pandas as pd
from google.genai.types import GenerateContentResponse
import ast

import llm
from models.response_models import (
    KeyComponents,
    Code,
    CodeJustification,
)
from system_path import SystemPath


def run_thematic_analysis(path: SystemPath, document_paths: list[str]):
    # New file
    with open(path.get_02_thematic_analysis_path(), "w") as f:
        f.write("")

    for document_path in document_paths:
        content = ""
        with open(document_path, "r") as f:
            content = f.read()

        response = generate_thematic_analysis(content, document_path)

        # Save extracted code (json text)
        with open(path.get_02_thematic_analysis_path(), "a+") as f:
            f.write(response.text)
            f.write("\n\n")

    print()
    print("-" * 50)
    print(
        f"Thematic analaysis text json result saved to: '{path.get_02_thematic_analysis_path()}'"
    )


def generate_thematic_analysis(
    content: str,
    document_path: str,
) -> GenerateContentResponse:

    prompt = f"""
Based on this transcript

{content}

Focus only "Participant" lines.
Perform thematic analysis and identify key codes and supporting quotes for Agent-Based Modeling system

Following these key components
{KeyComponents.get_explanation()}

Each component has at least {2} codes
Each code has maximum of {2} quotes. Quote must be exactly the same as original text and come from the same line.

file is {document_path}
"""
    response = llm.generate_content(
        prompt,
        response_schema=KeyComponents,
    )
    return response


def write_codes_csv_from_txt(path: SystemPath):
    # Read final raw codes
    with open(path.get_02_thematic_analysis_path(), "r") as f:
        content = f.read()

    # Write head of table
    codes_csv_path = path.get_02_thematic_analysis_csv_path()
    with open(codes_csv_path, "w") as f:
        f.write("File;Component;Code;Quote\n")

    # Write quotes (csv)
    for c in content.strip().split("\n\n"):
        document: dict = json.loads(c)

        for i, key in enumerate(KeyComponents.get_component_keys()):
            for code in document[key]:
                for quote in code["quotes"]:
                    component_name = KeyComponents.get_component_names()[i]
                    with open(codes_csv_path, "a+") as f:
                        f.write(
                            f"{document['file']};{component_name};{code['code']};{quote}\n"
                        )

    df = pd.read_csv(codes_csv_path, delimiter=";")
    df_sorted = df.sort_values(by="Component")  # sort by Component
    df_sorted.to_csv(codes_csv_path, index=False)  # index=False : no row name


def run_eabss_scope_finalisation(path: SystemPath):
    with open(path.get_01_objective_path(), "r") as f:
        objective_statement = f.read()
        objective_statement: dict = json.loads(objective_statement)
        objective = objective_statement["objective"]
        input = objective_statement["input"]
        output = objective_statement["output"]

    # Finalise key components
    with open(path.get_02_thematic_analysis_path(), "r") as f:
        text = f.read()

    component_dict = {}

    documents = text.strip().split("\n\n")
    for document_raw in documents:
        document: dict = json.loads(document_raw)
        for key in document.keys():
            if key not in component_dict:
                component_dict[key] = []

            for item in document[key]:
                component_dict[key].append(item)

    final_component_dict = {}
    for component in list(component_dict.keys()):
        if component != "file":
            response = generate_eabss_scope(
                component,
                component_dict[component],
                objective,
                input,
                output,
            )

            final_component_dict[component] = ast.literal_eval(response.text)

    # Save key component
    with open(path.get_02_eabss_scope_path(), "w") as f:
        f.write(json.dumps(final_component_dict, indent=4))

    print()
    print("-" * 50)
    print(f"EABSS components result saved to: '{path.get_02_eabss_scope_path()}'")
    print("\nPlease reivew and update the EABSS components if necessary.")


def generate_eabss_scope(
    component: str,
    codes_quotes: str,
    objective: str,
    input: str,
    output: str,
) -> GenerateContentResponse:
    # Finalise EABSS' given component
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}
    
Based on following codes & quotes of {component}

{codes_quotes}

Select minimum items from the codes & quotes that are the most important to build Agent-based modeling simulation with
Objective: {objective}
Experiment factors (inputs): {input}
Responses (outputs): {output}

The final codes & quotes has at least {1} codes
Each with justification why you select them
"""
    response = llm.generate_content(prompt, list[CodeJustification])

    return response


if __name__ == "__main__":
    path = SystemPath("travel2")
    document_paths = ["data/travel_scope_txt/Stage1_CreditonStLawrence1.txt"]
    # document_paths = ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]

    run_thematic_analysis(path, document_paths)
    # write_codes_csv_from_txt(path)
