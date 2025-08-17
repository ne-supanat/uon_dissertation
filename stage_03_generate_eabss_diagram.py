import llm
from models.response_models import (
    ScopeComponent,
    ScriptResponse,
)
import display_result

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
{ScopeComponent.get_explanation()}

{display_result.eabss_scope_result(path)}

Generate UML use case diagram of actors and key activities
Respond in mermaid.js format
Use flowchart LR
For actors and use cases use box element. For example, Actor1["Actor Title"]
To link them with arrow use -->
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def buidl_eabss_remaining_diagrams(path: SystemPath):
    with open(path.get_02_eabss_scope_path(), "r") as f:
        content = f.read()
        scope: ScopeComponent = ScopeComponent.model_validate_json(content)

    actors = [a.element for a in scope.actors]

    if len(actors) > 1:
        print(f"Please select the main actor to act as agents in the model")

        for i, actor in enumerate(actors):
            print(f"{i+1}. {actor}")

        choice = 0
        while not 1 <= choice <= len(actors):
            choice_str = input(
                f"\nEnter the actor number (1 - {len(actors)}): "
            ).lower()

            try:
                choice = int(choice_str)
            except:
                choice = 0
    else:
        choice = 1

    main_actor = actors[choice - 1]

    with open(path.get_03_eabss_main_actor_path(), "w") as f:
        f.write(main_actor)

    with open(path.get_03_eabss_usecase_diagram_path(), "r") as f:
        usecase_diagram = f.read()

    # actor class - UML class diagram
    class_diagram = generate_eabss_class_diagram(path, usecase_diagram, main_actor)
    with open(path.get_03_eabss_class_diagram_path(), "w") as f:
        f.write(class_diagram)

    # user state transition - UML state diagram (optional)
    state_transition_diagram = generate_eabss_state_transition_diagram(
        path, usecase_diagram, main_actor
    )
    with open(path.get_03_eabss_state_diagram_path(), "w") as f:
        f.write(state_transition_diagram)

    # key activities - UML activity diagram
    activity_diagram = generate_eabss_activity_diagram(
        path, usecase_diagram, main_actor
    )
    with open(path.get_03_eabss_activity_diagram_path(), "w") as f:
        f.write(activity_diagram)

    # interactions - UML sequence diagram
    interactions_diagram = generate_eabss_interaction_diagram(
        path, usecase_diagram, main_actor
    )
    with open(path.get_03_eabss_interaction_diagram_path(), "w") as f:
        f.write(interactions_diagram)

    print()
    print("-" * 50)
    for name, path in zip(
        [
            "Class diagram",
            "State transition diagram",
            "Activity diagram",
            "Interaction diagram",
        ],
        [
            path.get_03_eabss_class_diagram_path(),
            path.get_03_eabss_state_diagram_path(),
            path.get_03_eabss_activity_diagram_path(),
            path.get_03_eabss_interaction_diagram_path(),
        ],
    ):
        print("{:<25} {:<30}".format(name, f": saved to '{path}'"))
    print("\nPlease reivew and update the EABSS components if necessary.")


def generate_eabss_class_diagram(
    path: SystemPath, usecase_diagram: str, main_actor: str
):
    prompt = f"""
Following these key components
{ScopeComponent.get_explanation()}

{display_result.eabss_scope_result(path)}

Use case diagram:
{usecase_diagram}

Generate UML class diagram of "{main_actor}" that have relevant attributes and actions they might perform.
Respond in mermaid.js format
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def generate_eabss_state_transition_diagram(
    path: SystemPath, usecase_diagram: str, main_actor: str
):
    prompt = f"""
Following these key components
{ScopeComponent.get_explanation()}

{display_result.eabss_scope_result(path)}

And use case diagram
{usecase_diagram}

Generate state machine diagram of "{main_actor}" and Key activities
Respond in mermaid.js format
Use stateDiagram
For entry point use [*]
For state transition use -->

Example state transition of wake up and sleeping:
[*] --> Sleeping
Sleeping --> WakeUp: is morning 
WakeUp --> Sleeping: is night 
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def generate_eabss_activity_diagram(
    path: SystemPath, usecase_diagram: str, main_actor: str
):
    prompt = f"""
Following these key components
{ScopeComponent.get_explanation()}

{display_result.eabss_scope_result(path)}

And use case diagram
{usecase_diagram}

Generate UML activity diagram of "{main_actor}"
Respond in mermaid.js format
Use flowchart TD
For action use box element. For example, Action["Action"]
For decision node use diamond shape. For example, Decision{"{Decision}"}
To link them with arrow use -->
To have text in link use -- Text --> 
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def generate_eabss_interaction_diagram(
    path: SystemPath, usecase_diagram: str, main_actor: str
):
    prompt = f"""
Following these key components
{ScopeComponent.get_explanation()}

{display_result.eabss_scope_result(path)}

And use case diagram
{usecase_diagram}

Generate UML sequence diagram of "{main_actor}"
Respond in mermaid.js format
Use sequenceDiagram
For "{main_actor}" use actor {main_actor}
For other objects use participant Object
To show interaction link use ->> for solid line and -->> for dotted line
To add text in link use Actor->>Object: Text
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


if __name__ == "__main__":
    path = SystemPath("travel")

    # build_eabss_usecase_diagrams(path)
    buidl_eabss_remaining_diagrams(path)
