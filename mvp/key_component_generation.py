import llm


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


def generate():
    # # Finalise EABSS key components
    # with open(ta_codes_txt_path, "r") as f:
    #     codes = f.read()
    # ta.finalise_key_components(codes, objective, input, output)

    with open("mvp/results/key_components.txt", "r") as f:
        key_components = f.read()

    # # key activities - UML use case diagram
    # usecaseDiagram = drawKeyActivityUsecaseDiagram(keyComponents)
    # with open(f"mvp/results/usecase_diagram.txt", "w") as f:
    #     f.write(usecaseDiagram)

    # activityDiagram = drawActivityDiagram(keyComponents)
    # with open(f"mvp/results/activity_diagram.txt", "w") as f:
    #     f.write(activityDiagram)

    # # user state machine - UML state diagram
    # stateTransitionDiagram = drawStateTransition(keyComponents)
    # with open(f"mvp/results/state_transition_diagram.txt", "w") as f:
    #     f.write(stateTransitionDiagram)
