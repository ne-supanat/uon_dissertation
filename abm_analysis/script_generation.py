import llm
from response_models import KeyComponents, ScriptResponse, ThinkScriptResponse


def generate(
    objective: str,
    input: str,
    output: str,
    kc_scope_path: str,
    kc_usecase_diagram_path: str,
    kc_activity_diagram_path: str,
    kc_state_transition_diagram_path: str,
    kc_interaction_diagram_path: str,
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

    with open(kc_interaction_diagram_path, "r") as f:
        kc_interaction_diagram = f.read()

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

Generate a very simple NetLogo simulation script that can represent system based on UML diagrams
and can answer objective key
and response with output key at the end of simulation.

population is {100} and randomly assign with archetype
run for {100} tick

plot graph of chosen transportation each day
if script is if [] else [] change it to ifelse [] []

you don't have to setup plots
to update plot MUST use "update-visual"

when update plot, set current plot first then update value. this is an example

set-current-plot "Plot Name"

set-current-plot-pen "Pen name1"
plotxy ticks "value"

set-current-plot-pen "Pen name2"
plotxy ticks "value"

Please think first.
The generated script must not have functions named "update-plots", "setup-plots" in it
"""

    response: ScriptResponse = llm.generate_content(prompt, ThinkScriptResponse).parsed

    with open(simulation_script_path, "w") as f:
        f.write(response.script)


if __name__ == "__main__":
    folder_path = "abm_analysis/results"

    objective = "explore different usages of transportation from home to workplace"
    input = "traveller characteristic (transportation preference)"
    output = "number of used of each transportation type"

    kc_scope_path = folder_path + "/key_component_scope.txt"
    kc_usecase_diagram_path = folder_path + "/key_component_usecase_diagram.txt"
    kc_activity_diagram_path = folder_path + "/key_component_activity_diagram.txt"
    kc_state_transition_diagram_path = (
        folder_path + "/key_component_state_transition_diagram.txt"
    )
    kc_interaction_diagram_path = folder_path + "/key_component_interaction_diagram.txt"
    scenario_probability_path = folder_path + "/scenario_probability.csv"
    simulation_script_path = folder_path + "/simulation_script.txt"

    generate(
        objective,
        input,
        output,
        kc_scope_path,
        kc_usecase_diagram_path,
        kc_activity_diagram_path,
        kc_state_transition_diagram_path,
        kc_interaction_diagram_path,
        scenario_probability_path,
        simulation_script_path,
    )
