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
    physicalComponents: list[Code]
    socialAspect: list[Code]
    psychologicalAspect: list[Code]
    misc: list[Code]
    keyActivities: list[Code]

    def getComponentNames():
        return [
            "Actors",
            "Archetypes",
            "Physical Components",
            "Social Aspect",
            "Psychological Aspect",
            "Misc",
            "Key Activities",
        ]

    def getComponentKeys():
        return [
            "actors",
            "archetypes",
            "physicalComponents",
            "socialAspect",
            "psychologicalAspect",
            "misc",
            "keyActivities",
        ]


def thematic_analyse(
    interviewPaths: list[str], destinationPathTXT: str, destinationPathCSV: str
):
    # Write head of table
    with open(destinationPathCSV, "w") as f:
        f.write("File;Component;Code;Quote\n")

    for interviewPath in interviewPaths:
        interview = ""
        with open(interviewPath, "r") as f:
            interview = f.read()
        response = extract_key_components(interview, interviewPath)

        # Write raw response (json)
        with open(destinationPathTXT, "a+") as f:
            f.write(response.text)
            f.write("\n\n")

        # Write records for human review
        keyComponents: KeyComponents = response.parsed
        for i, component in enumerate(
            [
                keyComponents.actors,
                keyComponents.archetypes,
                keyComponents.physicalComponents,
                keyComponents.socialAspect,
                keyComponents.psychologicalAspect,
                keyComponents.misc,
                keyComponents.keyActivities,
            ]
        ):
            for code in component:
                for quote in code.quotes:
                    componentName = KeyComponents.getComponentNames()[i]

                    # Write quote as row record (csv)
                    with open(destinationPathCSV, "a+") as f:
                        f.write(
                            f"{interviewPath};{componentName};{code.code};{quote}\n"
                        )


def extract_key_components(
    interview: str,
    interviewPath: str,
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

filePath is {interviewPath}
"""
    response = llm.generateContent(
        prompt,
        response_schema=KeyComponents,
    )
    return response


def write_quotes_from_raw_txt(destinationPath: str):
    # Read final raw codes
    with open(f"mvp/results/codes_quotes_raw.txt", "r") as f:
        content = f.read()

    # Write head of table
    with open(destinationPath, "w") as f:
        f.write("File;Component;Code;Quote\n")

    # Write quotes (csv)
    for c in content.strip().split("\n\n"):
        component: dict = json.loads(c)

        for i, key in enumerate(KeyComponents.getComponentKeys()):
            for code in component[key]:
                for quote in code["quotes"]:
                    componentName = KeyComponents.getComponentNames()[i]
                    with open(destinationPath, "a+") as f:
                        f.write(
                            f"{component['file']};{componentName};{code['code']};{quote}\n"
                        )


if __name__ == "__main__":
    pass

    # thematic_analyse(
    #     ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"],
    #     destinationPathTXT="mvp/results/codes_quotes_raw.txt",
    #     destinationPathCSV="mvp/results/codes_quotes.csv",
    # )
    # write_quotes_from_raw_txt("mvp/results/codes_quotes_full.csv")
