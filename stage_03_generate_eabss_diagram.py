import os

import llm
from models.response_models import (
    KeyComponents,
    ScriptResponse,
)
import display_progress


def generate_diagrams(
    eabss_components_path,
    eabss_usecase_diagram_path,
    eabss_activity_diagram_path,
    eabss_state_transition_diagram_path,
    eabss_interaction_diagram_path,
    eabss_class_diagram_path,
):
    # key activities - UML use case diagram
    usecase_diagram = draw_usecase_diagram(
        eabss_components_path,
    )
    with open(eabss_usecase_diagram_path, "w") as f:
        f.write(usecase_diagram)

    # actor class - UML class diagram
    class_diagram = draw_class_diagram(
        eabss_components_path,
        usecase_diagram,
    )
    with open(eabss_class_diagram_path, "w") as f:
        f.write(class_diagram)

    # key activities - UML activity diagram
    activity_diagram = draw_activity_diagram(
        eabss_components_path,
        usecase_diagram,
    )
    with open(eabss_activity_diagram_path, "w") as f:
        f.write(activity_diagram)

    # user state machine - UML state diagram (optional)
    state_transition_diagram = draw_state_transition_diagram(
        eabss_components_path,
        usecase_diagram,
    )
    with open(eabss_state_transition_diagram_path, "w") as f:
        f.write(state_transition_diagram)

    # interactions - UML sequence diagram
    interactions_diagram = draw_interaction_diagram(
        eabss_components_path,
        usecase_diagram,
    )
    with open(eabss_interaction_diagram_path, "w") as f:
        f.write(interactions_diagram)

    # # # TODO: (optional) consider State condition table
    for name, path in zip(
        [
            "Use case diagram",
            "Activity diagram",
            "State transition diagram",
            # "State condition"
            "Interaction diagram",
            "Class diagram",
        ],
        [
            eabss_usecase_diagram_path,
            eabss_activity_diagram_path,
            eabss_state_transition_diagram_path,
            # eabss_state_condition_diagram_path
            eabss_interaction_diagram_path,
            eabss_class_diagram_path,
        ],
    ):
        print("{:<25} {:<30}".format(name, f": saved to '{path}'"))


def draw_usecase_diagram(key_component_path: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{display_progress.eabss_components_progress(key_component_path)}


generate very simple comprehensive UML usecase diagram
respond in mermaid.js format (use mermaid.js flowchart diagram to represent UML use case diagram)
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def draw_activity_diagram(key_component_path: str, usecase_diagram: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{display_progress.eabss_components_progress(key_component_path)}

And use case diagram
{usecase_diagram}

generate very simple comprehensive UML activity diagram
respond in mermaid.js format (use mermaid.js flowchart diagram to represent UML uactivity diagram)
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def draw_state_transition_diagram(key_component_path: str, usecase_diagram: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{display_progress.eabss_components_progress(key_component_path)}

And use case diagram
{usecase_diagram}

generate very simple comprehensive state machine diagram of Actors and Key activities
respond in mermaid.js format
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def draw_interaction_diagram(key_component_path: str, usecase_diagram: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{display_progress.eabss_components_progress(key_component_path)}

And use case diagram
{usecase_diagram}

generate very simple comprehensive UML sequence diagram of Actors
respond in mermaid.js format
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def draw_class_diagram(key_component_path: str, usecase_diagram: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{display_progress.eabss_components_progress(key_component_path)}

And use case diagram
{usecase_diagram}

generate very simple comprehensive UML class diagram of Actors that have relevant attributes and actions they might perform.
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
    eabss_class_diagram_path = os.path.join(
        results_path, "eabss_diagram_class_diagram.txt"
    )

    # generate_components(
    #     objective_statement_path,
    #     ta_codes_txt_path,
    #     eabss_components_path,
    # )

    generate_diagrams(
        eabss_components_path,
        eabss_usecase_diagram_path,
        eabss_activity_diagram_path,
        eabss_state_transition_diagram_path,
        eabss_interaction_diagram_path,
        eabss_class_diagram_path,
    )
