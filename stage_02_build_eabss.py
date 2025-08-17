import json
import pandas as pd
from google.genai.types import GenerateContentResponse
import ast
import display_result

import utils
import llm
from models.response_models import (
    ScopeThemeCode,
    ScopeComponent,
    ScopeElement,
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

Perform thematic analysis and identify key theme codes and supporting quotes for Agent-Based Modeling system

Following these key components
{ScopeComponent.get_explanation()}

The codes must be in this format "Theme Code" NOT "ThemeCode"
Each component has at least {2} codes
Each theme code has maximum of {2} quotes. 
Each quote must be a sentence or sentences that exactly the same and in one speaking line from the original transcript.

file is {document_path}
"""
    response = llm.generate_content(
        prompt,
        response_schema=ScopeThemeCode,
    )
    return response


# TODO: remove if not used
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

        for i, key in enumerate(ScopeThemeCode.get_component_keys()):
            for code in document[key]:
                for quote in code["quotes"]:
                    component_name = ScopeThemeCode.get_component_names()[i]
                    with open(codes_csv_path, "a+") as f:
                        f.write(
                            f"{document['file']};{component_name};{code['code']};{quote}\n"
                        )

    df = pd.read_csv(codes_csv_path, delimiter=";")
    df_sorted = df.sort_values(by="Component")  # sort by Component
    df_sorted.to_csv(codes_csv_path, index=False)  # index=False : no row name


def run_eabss_scope_finalisation(path: SystemPath):
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
                path,
                component,
                component_dict[component],
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
    path: str,
    component_key: str,
    codes_quotes: list[dict],
) -> GenerateContentResponse:
    component_name = ScopeThemeCode.get_component_name_from_key(component_key)

    theme_codes_str = ""
    for theme_code in codes_quotes:
        theme_codes_str += theme_code["code"] + "\n"
        theme_codes_str += "".join([f"- {quote}\n" for quote in theme_code["quotes"]])
        theme_codes_str += "\n"

    # Finalise EABSS' given component
    prompt = f"""
Based on EABSS scope components
{ScopeThemeCode.get_explanation()}

Using following Theme codes & quotes of "{component_name}"

{theme_codes_str}

and Model's outline
{display_result.topic_outline_result(path)}

Select minimum items from the theme codes & quotes that are the most important to build Agent-based modelling simulation

The codes (element) must be in this format "Theme Code" NOT "ThemeCode"
The final theme codes & quotes must have at least {1} code
Each with theme codes short description and brief justification of why you select them
"""
    response = llm.generate_content(prompt, list[ScopeElement])
    return response


if __name__ == "__main__":
    path = SystemPath("travel")

    document_paths = utils.get_transcript_file_paths(
        path.get_scope_data_directory_path()
    )

    run_thematic_analysis(path, document_paths)
    run_eabss_scope_finalisation(path)
    # write_codes_csv_from_txt(path)
