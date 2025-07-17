import os
import json
import ast
from google.genai.types import GenerateContentResponse

import llm
from models.response_models import (
    KeyComponents,
    ScriptResponse,
    Code,
    CodeJustification,
)


def generate_components(
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

    print(f"\nEABSS components result saved to: '{eabss_components_path}'")
    print("Please reivew and update the EABSS components if necessary.")


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


def finalise_eabss_component(
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
Each code has maximum all relevant quotes
"""
    response = llm.generate_content(prompt, list[Code])

    return response


def generate_diagrams(
    eabss_components_path,
    eabss_usecase_diagram_path,
    eabss_activity_diagram_path,
    eabss_state_transition_diagram_path,
    eabss_interaction_diagram_path,
):
    with open(eabss_components_path, "r") as f:
        key_components = f.read()

    # key activities - UML use case diagram
    usecase_diagram = draw_usecase_diagram(key_components)
    with open(eabss_usecase_diagram_path, "w") as f:
        f.write(usecase_diagram)

    activity_diagram = draw_activity_diagram(key_components)
    with open(eabss_activity_diagram_path, "w") as f:
        f.write(activity_diagram)

    # user state machine - UML state diagram
    state_transition_diagram = draw_state_transition_diagram(key_components)
    with open(eabss_state_transition_diagram_path, "w") as f:
        f.write(state_transition_diagram)

    # interactions - UML sequence diagram
    interactions_diagram = draw_interaction_diagram(key_components)
    with open(eabss_interaction_diagram_path, "w") as f:
        f.write(interactions_diagram)

    # TODO: (optional) consider State condition table
    for name, path in zip(
        [
            "Use case diagram",
            "Activity diagram",
            "State transition diagram",
            # "State condition"
            "Interaction diagram",
        ],
        [
            eabss_usecase_diagram_path,
            eabss_activity_diagram_path,
            eabss_state_transition_diagram_path,
            # eabss_interaction_diagram_path
            eabss_interaction_diagram_path,
        ],
    ):
        print("{:<25} {:<30}".format(name, f": saved to '{path}'"))


def draw_usecase_diagram(key_component: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{key_component}

generate very simple comprehensive UML usecase diagram
respond in mermaid.js format (use mermaid.js flowchart diagram to represent UML use case diagram)
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def draw_activity_diagram(key_component: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{key_component}

generate very simple comprehensive UML activity diagram
respond in mermaid.js format (use mermaid.js flowchart diagram to represent UML uactivity diagram)
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def draw_state_transition_diagram(key_component: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{key_component}

generate very simple comprehensive state machine diagram of Actors and Key activities
respond in mermaid.js format
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def draw_interaction_diagram(key_component: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{key_component}

generate very simple comprehensive UML sequence diagram of Actors
respond in mermaid.js format
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


if __name__ == "__main__":
    results_path = "results_2"
    objective_statement_path = os.path.join(results_path, "objective.txt")
    ta_codes_txt_path = os.path.join(results_path, "thematic_analysis_codes.txt")
    eabss_components_path = os.path.join(results_path, "eabss_scope.txt")
    eabss_usecase_diagram_path = os.path.join(
        results_path, "eabss_diagram_usecase_diagram.txt"
    )
    eabss_activity_diagram_path = os.path.join(
        results_path, "eabss_diagram_activity_diagram.txt"
    )
    eabss_state_transition_diagram_path = os.path.join(
        results_path, "eabss_diagram_state_diagram.txt"
    )
    eabss_interaction_diagram_path = os.path.join(
        results_path, "eabss_diagram_interaction_diagram.txt"
    )

    generate_components(
        objective_statement_path,
        ta_codes_txt_path,
        eabss_components_path,
    )

    generate_diagrams(
        eabss_components_path,
        eabss_usecase_diagram_path,
        eabss_activity_diagram_path,
        eabss_state_transition_diagram_path,
        eabss_interaction_diagram_path,
    )
