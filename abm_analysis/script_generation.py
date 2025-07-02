import llm
from response_models import KeyComponents, ScriptResponse


def generate(
    objective: str,
    input: str,
    output: str,
    kc_scope_path: str,
    kc_usecase_diagram_path: str,
    kc_activity_diagram_path: str,
    kc_state_transition_diagram_path: str,
    scenario_probability_path: str,
    simulation_script_path: str,
):
    with open(kc_scope_path, "r") as f:
        kc_scope = f.read()

    with open(kc_usecase_diagram_path, "r") as f:
        kc_usecase = f.read()

    with open(kc_activity_diagram_path, "r") as f:
        kc_activity = f.read()

    with open(kc_state_transition_diagram_path, "r") as f:
        kc_state_transition = f.read()

    with open(scenario_probability_path, "r") as f:
        action_probability = f.read()

    prompt = f"""
Based on these EABSS key components

{KeyComponents.get_explanation()}

This model scope is
{kc_scope}

Objective
{objective}

Input
{input}

Output
{output}

UML use case diagram
{kc_usecase}

UML activity diagram
{kc_activity}

UML state transition diagram
{kc_state_transition}

Archetype action probability
{action_probability}

Generate a very simple NetLogo simulation script.
population is {100} and randomly assign with archetype
run for {100} tick
print chosen transportation each day
plot graph of chosen transportation each day

if script is if [] else [] change it to ifelse [] []

to update plot use use update-plot not update-plots
when update plot, set current plot first then update value. this is an example

set-current-plot-pen "Pen name"
plotxy ticks "value"
"""

    response: ScriptResponse = llm.generate_content(prompt, ScriptResponse).parsed

    with open(simulation_script_path, "w") as f:
        f.write(response.script)
