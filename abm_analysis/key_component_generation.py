import llm
from response_models import KeyComponents, ScriptResponse


def finalise_key_components(
    codes_quotes: str,
    objective: str,
    input: str,
    output: str,
):
    prompt = f"""
Based on following codes and quotes

{codes_quotes}

Following these key components
{KeyComponents.get_explanation()}

Select minimum items from each each components that are the most important to build Agent-based modeling simulation with
Objective: {objective}
Experiment factors (inputs): {input}
Responses (outputs): {output}

Each component has minimum of {2} codes
Each code has maximum all relevant quotes

file is {None}
"""
    response = llm.generate_content(prompt, KeyComponents)

    # Save key component
    with open(f"abm_analysis/results/key_component_scope.txt", "w") as f:
        f.write(response.text)


def draw_usecase_diagram(key_component: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{key_component}

generate very simple comprehensive UML usecase diagram
response in mermaid.js format (mermaid.js might not support have diagram called use case diagram. use any diagram that can represent UML use case diagram)
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def draw_activity_diagram(key_component: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{key_component}

generate very simple comprehensive UML activity diagram
response in mermaid.js format (mermaid.js might not support have diagram called activity diagram. use any diagram that can represent UML uactivity diagram)
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def draw_state_transition_diagram(key_component: str):
    prompt = f"""
Following these key components
{KeyComponents.get_explanation()}

{key_component}

generate very simple comprehensive UML state transition diagram
response in mermaid.js format
"""
    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed
    return response.script


def generate(
    objective,
    input,
    output,
    thematic_analysis_codes_txt_path,
    key_component_scope_path,
    key_component_usecase_diagram_path,
    key_component_activity_diagram_path,
    key_component_state_transition_diagram_path,
):
    # Finalise key components
    with open(thematic_analysis_codes_txt_path, "r") as f:
        codes = f.read()
    finalise_key_components(codes, objective, input, output)

    with open(key_component_scope_path, "r") as f:
        key_components = f.read()

    # print(key_components)

    # key activities - UML use case diagram
    usecaseDiagram = draw_usecase_diagram(key_components)
    with open(key_component_usecase_diagram_path, "w") as f:
        f.write(usecaseDiagram)

    activityDiagram = draw_activity_diagram(key_components)
    with open(key_component_activity_diagram_path, "w") as f:
        f.write(activityDiagram)

    # user state machine - UML state diagram
    stateTransitionDiagram = draw_state_transition_diagram(key_components)
    with open(key_component_state_transition_diagram_path, "w") as f:
        f.write(stateTransitionDiagram)


if __name__ == "__main__":
    # Objective
    objective = "explore different usages of transportation from home to workplace"

    # Input
    input = "traveller characteristic (transportation preference)"

    # Output
    output = "number of used of each transportation type"

    ta_codes_txt_path = "abm_analysis/results/thematic_analysis_codes.txt"
    kc_scope_path = "abm_analysis/results/key_component_scope.txt"
    kc_usecase_diagram_path = "abm_analysis/results/key_component_usecase_diagram.txt"
    kc_activity_diagram_path = "abm_analysis/results/key_component_activity_diagram.txt"
    kc_state_transition_diagram_path = (
        "abm_analysis/results/key_component_state_transition_diagram.txt"
    )

    generate(
        objective,
        input,
        output,
        ta_codes_txt_path,
        kc_scope_path,
        kc_usecase_diagram_path,
        kc_activity_diagram_path,
        kc_state_transition_diagram_path,
    )
