import os
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


def analyse(document_paths: list[str], destination_path_txt: str):
    # New file
    with open(destination_path_txt, "w") as f:
        f.write("")

    for document_path in document_paths:
        document = ""
        with open(document_path, "r") as f:
            document = f.read()
        response = extract_key_components(document, document_path)

        # Save extracted code (json text)
        with open(destination_path_txt, "a+") as f:
            f.write(response.text)
            f.write("\n\n")

    print()
    print("-" * 50)
    print(f"Thematic analaysis text json result saved to: '{destination_path_txt}'")


def extract_key_components(
    document: str,
    document_path: str,
) -> GenerateContentResponse:

    prompt = f"""
Based on this transcript

{document}

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


def write_codes_csv_from_txt(codes_txt_path, codes_csv_path: str):
    # Read final raw codes
    with open(codes_txt_path, "r") as f:
        content = f.read()

    # Write head of table
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


def generate_final_components(
    objective_statement_path,
    thematic_analysis_codes_txt_path,
    eabss_components_path,
):
    with open(objective_statement_path, "r") as f:
        objective_statement = f.read()
        objective_statement: dict = json.loads(objective_statement)
        objective = objective_statement["objective"]
        input = objective_statement["input"]
        output = objective_statement["output"]

    # Finalise key components
    with open(thematic_analysis_codes_txt_path, "r") as f:
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
            response = finalise_eabss_component_justification(
                component,
                component_dict[component],
                objective,
                input,
                output,
            )

            final_component_dict[component] = ast.literal_eval(response.text)

    # Save key component
    with open(eabss_components_path, "w") as f:
        f.write(json.dumps(final_component_dict, indent=4))

    print()
    print("-" * 50)
    print(f"EABSS components result saved to: '{eabss_components_path}'")
    print("\nPlease reivew and update the EABSS components if necessary.")


def finalise_eabss_component_justification(
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

The final codes & quotes has at least {2} codes
Each with justification why you select them
"""
    response = llm.generate_content(prompt, list[CodeJustification])

    return response


if __name__ == "__main__":
    document_paths = ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]

    results_path = "results_5"
    ta_codes_txt_path = os.path.join(results_path, "02_thematic_analysis_codes.txt")
    ta_codes_csv_path = os.path.join(results_path, "02_thematic_analysis_codes.csv")

    analyse(
        document_paths,
        ta_codes_txt_path,
        ta_codes_csv_path,
    )

    # write_codes_csv_from_txt(
    #     ta_codes_txt_path,
    #     ta_codes_csv_path,
    # )
