import json
from google.genai.types import GenerateContentResponse

import llm
from response_models import KeyComponents


def analyse(
    document_paths: list[str], destination_path_txt: str, destination_path_csv: str
):
    # Write head of table
    with open(destination_path_csv, "w") as f:
        f.write("File;Component;Code;Quote\n")

    for document_path in document_paths:
        document = ""
        with open(document_path, "r") as f:
            document = f.read()
        response = extract_key_components(document, document_path)

        # Write raw response (json)
        with open(destination_path_txt, "a+") as f:
            f.write(response.text)
            f.write("\n\n")

        # Write records for human review
        key_components: KeyComponents = response.parsed
        for i, component in enumerate(
            [
                key_components.actors,
                key_components.archetypes,
                key_components.physical_components,
                key_components.social_aspect,
                key_components.psychological_aspect,
                key_components.misc,
                key_components.key_activities,
            ]
        ):
            for code in component:
                for quote in code.quotes:
                    component_name = KeyComponents.get_component_names()[i]

                    # Write quote as row record (csv)
                    with open(destination_path_csv, "a+") as f:
                        f.write(
                            f"{document_path};{component_name};{code.code};{quote}\n"
                        )


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

Each component has minimum of {2} codes
Each code has maximum of {2} quotes

file is {document_path}
"""
    response = llm.generate_content(
        prompt,
        response_schema=KeyComponents,
    )
    return response


def write_codes_csv_from_txt(codes_txt_path, destination_path: str):
    # Read final raw codes
    with open(codes_txt_path, "r") as f:
        content = f.read()

    # Write head of table
    with open(destination_path, "w") as f:
        f.write("File;Component;Code;Quote\n")

    # Write quotes (csv)
    for c in content.strip().split("\n\n"):
        component: dict = json.loads(c)

        for i, key in enumerate(KeyComponents.get_component_keys()):
            for code in component[key]:
                for quote in code["quotes"]:
                    component_name = KeyComponents.get_component_names()[i]
                    with open(destination_path, "a+") as f:
                        f.write(
                            f"{component['file']};{component_name};{code['code']};{quote}\n"
                        )


if __name__ == "__main__":
    document_paths = ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    analyse(
        document_paths,
        "mvp/results/thematic_analysis_codes.txt",
        "mvp/results/thematic_analysis_codes.csv",
    )
    write_codes_csv_from_txt(
        "mvp/results/thematic_analysis_codes.txt",
        "mvp/results/thematic_analysis_codes_sum.csv",
    )
