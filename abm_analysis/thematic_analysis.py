import json
import pandas as pd
from google.genai.types import GenerateContentResponse

import llm
from response_models import KeyComponents


def analyse(
    document_paths: list[str], destination_path_txt: str, destination_path_csv: str
):
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

        # Save extracted code (csv format)
        write_codes_csv_from_txt(
            destination_path_txt,
            destination_path_csv,
        )

    print(f"Thematic analaysis text json result saved to: '{destination_path_txt}'")
    print(f"Thematic analaysis csv result saved to: '{destination_path_csv}'")


def extract_key_components(
    document: str,
    document_path: str,
) -> GenerateContentResponse:

    prompt = f"""
Based on this transcript

{document}

Focus only participant responses.
Perform thematic analysis and identify key codes and supporting quotes for Agent-Based Modeling system

Following these key components
{KeyComponents.get_explanation()}

Each component has at least {2} codes
Each code has maximum of {2} quotes

Except Archetype component.
For Archetype component, please classify participant an archetype.

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


if __name__ == "__main__":
    document_paths = ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    # analyse(
    #     document_paths,
    #     "abm_analysis/results/thematic_analysis_codes.txt",
    #     "abm_analysis/results/thematic_analysis_codes.csv",
    # )

    write_codes_csv_from_txt(
        "abm_analysis/results_2/thematic_analysis_codes.txt",
        "abm_analysis/results_2/thematic_analysis_codes.csv",
    )
