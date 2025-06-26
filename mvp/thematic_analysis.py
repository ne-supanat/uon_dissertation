import json
from pydantic import BaseModel
from google.genai.types import GenerateContentResponse

import llm


class Code(BaseModel):
    code: str
    quotes: list[str]


class KeyComponents(BaseModel):
    file: str
    actors: list[Code]
    archetypes: list[Code]
    physical_components: list[Code]
    social_aspect: list[Code]
    psychological_aspect: list[Code]
    misc: list[Code]
    key_activities: list[Code]

    def get_component_names():
        return [
            "Actors",
            "Archetypes",
            "Physical Components",
            "Social Aspect",
            "Psychological Aspect",
            "Misc",
            "Key Activities",
        ]

    def get_component_keys():
        return [
            "actors",
            "archetypes",
            "physical_components",
            "social_aspect",
            "psychological_aspect",
            "misc",
            "key_activities",
        ]


def thematic_analyse(
    interview_paths: list[str], destination_path_txt: str, destination_path_csv: str
):
    # Write head of table
    with open(destination_path_csv, "w") as f:
        f.write("File;Component;Code;Quote\n")

    for interview_path in interview_paths:
        interview = ""
        with open(interview_path, "r") as f:
            interview = f.read()
        response = extract_key_components(interview, interview_path)

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
                            f"{interview_path};{component_name};{code.code};{quote}\n"
                        )


def extract_key_components(
    interview: str,
    interview_path: str,
) -> GenerateContentResponse:

    prompt = f"""
Based on this transcript

{interview}

Focus only participant responses.
Perform thematic analysis and identify key codes and supporting quotes for Agent-Based Modeling system

Following these key components
-	Actors are agents which can be a person or groups or organisation inside the system
-	Archetypes are categories of Actors defines what they are allowed or expected to do
-	Physical components are objects or tools or systems that actors use
-	Social aspect is rules or norms about social behaviour
-   Psychological aspect is rules or norms about psychological behaviour
-   Misc are real world elements that do not fall in any component

-	Key activities are interactions between actors and actors or actors and system environment


Each component has minimum of {2} codes
Each code has maximum of {2} quotes

filePath is {interview_path}
"""
    response = llm.generate_content(
        prompt,
        response_schema=KeyComponents,
    )
    return response


def write_quotes_from_raw_txt(destination_path: str):
    # Read final raw codes
    with open(f"mvp/results/codes_quotes_raw.txt", "r") as f:
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
    pass

    # thematic_analyse(
    #     ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"],
    #     destination_path_txt="mvp/results/codes_quotes_raw.txt",
    #     destination_path_csv="mvp/results/codes_quotes.csv",
    # )
    write_quotes_from_raw_txt("mvp/results/codes_quotes_full.csv")
