import llm
from models.response_models import ScopeThemeCode, ThinkScriptResponse
import display_result
from models.archetypes import Archetype

from system_path import SystemPath


def build_simulation_script(path: SystemPath):
    with open(path.get_03_model_usecase_diagram_path(), "r") as f:
        usecase_diagram = f.read()

    with open(path.get_03_model_class_diagram_path(), "r") as f:
        class_diagram = f.read()

    with open(path.get_03_model_activity_diagram_path(), "r") as f:
        activity_diagram = f.read()

    with open(path.get_03_model_state_diagram_path(), "r") as f:
        state_transition_diagram = f.read()

    with open(path.get_03_model_interaction_diagram_path(), "r") as f:
        interaction_diagram = f.read()

    response = generate_simulation_script(
        path,
        usecase_diagram,
        activity_diagram,
        state_transition_diagram,
        interaction_diagram,
        class_diagram,
    )

    with open(path.get_07_simulation_script_think_path(), "w") as f:
        f.write(response.think)
    with open(path.get_07_simulation_script_path(), "w") as f:
        f.write(response.script)

    print()
    print("-" * 50)
    print(
        f"Simulation script reasoning result saved to: '{path.get_07_simulation_script_think_path()}'"
    )
    print(
        f"Simulation script result saved to: '{path.get_07_simulation_script_path()}'\n"
    )
    print("Please reivew and update the generated simulation script if necessary.")
    print(
        "If there are errors or need some improvements consider do it manually or use LLMs e.g. ChatGPT"
    )


def generate_simulation_script(
    path: SystemPath,
    usecase_diagram,
    activity_diagram,
    state_transition_diagram,
    interaction_diagram,
    class_diagram,
) -> ThinkScriptResponse:
    prompt = f"""
Based on these EABSS key components:
{ScopeThemeCode.get_explanation()}

And following model detail:
{display_result.topic_outline_result(path)}
{display_result.model_scope_result(path)}
Use case diagram:
{usecase_diagram}
{"-"*50}
Class diagram:
{class_diagram}
{"-"*50}
Activity diagram:
{activity_diagram}
{"-"*50}
State transition diagram:
{state_transition_diagram}
{"-"*50}
Interaction diagram:
{interaction_diagram}
{"-"*50}
Archetype action probability
{display_result.decision_probability_table_result(path)}

Generate a NetLogo simulation script that can represent system based on UML diagrams
and can answer objective key
and respond with output key at the end of simulation.

{"-"*50}
Follow this NetLogo template:

turtles-own [
  archetype
]

globals [
  ; misc elements
]

to setup
    clear-all

    create-turtles {100} [
        setxy random-xcor random-ycor
        set shape "person"

        ; Randomly assign an archetype
        let archetype-index random {len([a for a in Archetype])}
        (ifelse
    {"".join([f"""
        archetype-index = {i} [
            set color {5+(i*10)%140}
            set archetype "{archetype.value}"
        ]""" for i, archetype in enumerate([archetype for archetype in Archetype])])}
        
        )
    ]
    reset-ticks
end

to go
    tick

    ;ask turtle to do "Key activities"

    save
    if ticks = {500} [stop]
end

to activity
    ; actions
end
 
to save
    file-open "outputs.csv"
    
    ; file-print outputs
    
    file-close
end

{"-"*50}

Save output should use file-print. So, It has no double-quote and ready to be used in CSV format
This is NetLogo Language not Python. The way writing if-else is different.
"""

    response = llm.generate_content(prompt, ThinkScriptResponse).parsed
    return response


if __name__ == "__main__":
    path = SystemPath("travel")
    build_simulation_script(path)
