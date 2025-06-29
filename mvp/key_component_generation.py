import llm
from response_models import KeyComponents


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
Input: {input}
Output: {output}

Each component has minimum of {2} codes
Each code has maximum all relevant quotes

file is {None}
"""
    print(prompt)
    response = llm.generate_content(prompt, KeyComponents)

    # Save key component
    with open(f"mvp/results/key_component_scope.txt", "w") as f:
        f.write(response.text)


def draw_usecase_diagram(key_component: str):
    prompt = f"""
Based on following Engineering Agent-Based Social Simulations (EABSS) key components

{key_component}

generate UML use case diagram for all key activities
response in plantUML format
"""
    response = llm.generate_content(prompt)
    return response.text


def draw_activity_diagram(key_component: str):
    prompt = f"""
Based on following Engineering Agent-Based Social Simulations (EABSS) key components

{key_component}

generate UML activity diagram for all key activities
response in plantUML format
"""
    response = llm.generate_content(prompt)
    return response.text


def draw_state_transition_diagram(key_component: str):
    prompt = f"""
Based on following Engineering Agent-Based Social Simulations (EABSS) key components

{key_component}

generate UML state transition diagram of actor acretype if needed
response in plantUML format
"""
    response = llm.generate_content(prompt)
    return response.text


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

    print(key_components)

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

    # Input, Output
    input = (
        "traveller characteristic (age, gender, occupation, transportation preference)"
    )

    output = "number of used of each transportation type"
    ta_codes_txt_path = "mvp/results/thematic_analysis_codes.txt"
    kc_scope_path = "mvp/results/key_component_scope.txt"
    kc_usecase_diagram_path = "mvp/results/key_component_usecase_diagram.txt"
    kc_activity_diagram_path = "mvp/results/key_component_activity_diagram.txt"
    kc_state_transition_diagram_path = (
        "mvp/results/key_component_state_transition_diagram.txt"
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
