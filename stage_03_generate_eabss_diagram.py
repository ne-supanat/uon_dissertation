import llm
from models.response_models import (
    KeyComponents,
    ScriptResponse,
)
import display_progress

from system_path import SystemPath


def build_eabss_usecase_diagrams(path: SystemPath):
    # key activities - UML use case diagram
    usecase_diagram = generate_eabss_usecase_diagram(path)
    with open(path.get_03_eabss_usecase_diagram_path(), "w") as f:
        f.write(usecase_diagram)

    print()
    print("-" * 50)
    print(
        "{:<25} {:<30}".format(
            "Use case diagram",
            f": saved to '{path.get_03_eabss_usecase_diagram_path()}'",
        )
    )
    print("\nPlease reivew and update the use case diagram if necessary.")


def generate_eabss_usecase_diagram(path: SystemPath):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{display_progress.eabss_components_progress(path)}

generate very simple comprehensive UML usecase diagram
respond in mermaid.js format (use mermaid.js flowchart diagram to represent UML use case diagram)
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def buidl_eabss_remaining_diagrams(path: SystemPath):
    with open(path.get_03_eabss_usecase_diagram_path(), "r") as f:
        usecase_diagram = f.read()

    # actor class - UML class diagram
    class_diagram = generate_eabss_class_diagram(path, usecase_diagram)
    with open(path.get_03_eabss_class_diagram_path(), "w") as f:
        f.write(class_diagram)

    # key activities - UML activity diagram
    activity_diagram = generate_eabss_activity_diagram(path, usecase_diagram)
    with open(path.get_03_eabss_activity_diagram_path(), "w") as f:
        f.write(activity_diagram)

    # user state transition - UML state diagram (optional)
    state_transition_diagram = generate_eabss_state_transition_diagram(
        path, usecase_diagram
    )
    with open(path.get_03_eabss_state_diagram_path(), "w") as f:
        f.write(state_transition_diagram)

    # interactions - UML sequence diagram
    interactions_diagram = generate_eabss_interaction_diagram(path, usecase_diagram)
    with open(path.get_03_eabss_interaction_diagram_path(), "w") as f:
        f.write(interactions_diagram)

    # TODO: (optional) consider State condition table
    print()
    print("-" * 50)
    for name, path in zip(
        [
            "Activity diagram",
            "State transition diagram",
            # "State condition"
            "Interaction diagram",
            "Class diagram",
        ],
        [
            path.get_03_eabss_class_diagram_path(),
            path.get_03_eabss_activity_diagram_path(),
            path.get_03_eabss_state_diagram_path(),
            # eabss_state_condition_diagram_path
            path.get_03_eabss_interaction_diagram_path(),
        ],
    ):
        print("{:<25} {:<30}".format(name, f": saved to '{path}'"))
    print("\nPlease reivew and update the EABSS components if necessary.")


def generate_eabss_class_diagram(path: SystemPath, usecase_diagram: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{display_progress.eabss_components_progress(path)}

And use case diagram
{usecase_diagram}

generate very simple comprehensive UML class diagram of Actors that have relevant attributes and actions they might perform.
respond in mermaid.js format
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def generate_eabss_activity_diagram(path: SystemPath, usecase_diagram: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{display_progress.eabss_components_progress(path)}

And use case diagram
{usecase_diagram}

generate very simple comprehensive UML activity diagram
respond in mermaid.js format (use mermaid.js flowchart diagram to represent UML uactivity diagram)
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def generate_eabss_state_transition_diagram(path: SystemPath, usecase_diagram: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{display_progress.eabss_components_progress(path)}

And use case diagram
{usecase_diagram}

generate very simple comprehensive state machine diagram of Actors and Key activities
respond in mermaid.js format
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def generate_eabss_interaction_diagram(path: SystemPath, usecase_diagram: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{display_progress.eabss_components_progress(path)}

And use case diagram
{usecase_diagram}

generate very simple comprehensive UML sequence diagram of Actors
respond in mermaid.js format
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


if __name__ == "__main__":
    path = SystemPath("results_2")

    build_eabss_usecase_diagrams(path)
    buidl_eabss_remaining_diagrams(path)
