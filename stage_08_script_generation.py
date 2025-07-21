import os

import llm
from models.response_models import KeyComponents, ScriptResponse, ThinkScriptResponse
import display_progress
from models.archetypes import Archetype


def generate(
    objective_statement_path,
    eabss_components_path,
    eabss_usecase_diagram_path,
    eabss_activity_diagram_path,
    eabss_state_transition_diagram_path,
    eabss_interaction_diagram_path,
    eabss_class_diagram_path,
    archetype_path,
    scenario_questions_path,
    scenario_choices_path,
    decision_probability_path,
    simulation_script_think_path,
    simulation_script_path,
):
    with open(eabss_usecase_diagram_path, "r") as f:
        eabss_usecase_diagram = f.read()

    with open(eabss_activity_diagram_path, "r") as f:
        eabss_activity_diagram = f.read()

    with open(eabss_state_transition_diagram_path, "r") as f:
        eabss_state_transition_diagram = f.read()

    with open(eabss_interaction_diagram_path, "r") as f:
        eabss_interaction_diagram = f.read()

    with open(eabss_class_diagram_path, "r") as f:
        eabss_class_diagram = f.read()

    response = generate_script(
        objective_statement_path,
        eabss_components_path,
        eabss_usecase_diagram,
        eabss_activity_diagram,
        eabss_state_transition_diagram,
        eabss_interaction_diagram,
        eabss_class_diagram,
        archetype_path,
        scenario_questions_path,
        scenario_choices_path,
        decision_probability_path,
    )

    with open(simulation_script_think_path, "w") as f:
        f.write(response.think)
    with open(simulation_script_path, "w") as f:
        f.write(response.script)

    print(
        f"\nSimulation script reasoning result saved to: '{simulation_script_think_path}'"
    )
    print(f"Simulation script result saved to: '{simulation_script_path}'\n")
    print("Please reivew and update the generated simulation script if necessary.")
    print(
        "If there are errors or need some improvements consider do it manually or use LLMs e.g. ChatGPT"
    )


def generate_script(
    objective_statement_path,
    eabss_components_path,
    eabss_usecase_diagram,
    eabss_activity_diagram,
    eabss_state_transition_diagram,
    eabss_interaction_diagram,
    eabss_class_diagram,
    archetype_path,
    scenario_questions_path,
    scenario_choices_path,
    decision_probability_path,
) -> ThinkScriptResponse:
    prompt = f"""
Based on these EABSS key components:
{KeyComponents.get_explanation()}

And following model detail:
{display_progress.objective_statement_progress(objective_statement_path)}
{display_progress.eabss_components_progress(eabss_components_path)}
Use case diagram:
{eabss_usecase_diagram}
{"-"*50}
Class diagram:
{eabss_class_diagram}
{"-"*50}
Activity diagram:
{eabss_activity_diagram}
{"-"*50}
State transition diagram:
{eabss_state_transition_diagram}
{"-"*50}
Interaction diagram:
{eabss_interaction_diagram}
{"-"*50}
Archetype action probability
{display_progress.archetype_progess(archetype_path)}
{display_progress.scenario_progess(scenario_questions_path, scenario_choices_path)}
{display_progress.decision_probability_table_progess(decision_probability_path)}

Generate a very simple NetLogo simulation script that can represent system based on UML diagrams
and can answer objective key
and respond with output key at the end of simulation.

{"-"*50}
Follow this NetLogo template:

turtles-own [
  archetype
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
    results_path = "results_2"

    objective_statement_path = os.path.join(results_path, "objective.txt")

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
    # TODO: (optional) add transition table
    # eabss_state_transition_table_path = os.path.join(results_path,"eabss_diagram_state_table.txt")
    eabss_interaction_diagram_path = os.path.join(
        results_path, "eabss_diagram_interaction_diagram.txt"
    )
    archetype_path = os.path.join(results_path, "archetype.txt")
    scenario_questions_path = os.path.join(results_path, "scenario_questions.txt")
    scenario_choices_path = os.path.join(results_path, "scenario_choices.txt")
    decision_probability_path = os.path.join(results_path, "scenario_probability.csv")
    simulation_script_think_path = os.path.join(
        results_path, "simulation_script_think.txt"
    )
    simulation_script_path = os.path.join(results_path, "simulation_script.txt")

    generate(
        objective_statement_path,
        eabss_components_path,
        eabss_usecase_diagram_path,
        eabss_activity_diagram_path,
        eabss_state_transition_diagram_path,
        eabss_interaction_diagram_path,
        archetype_path,
        scenario_questions_path,
        scenario_choices_path,
        decision_probability_path,
        simulation_script_think_path,
        simulation_script_path,
    )
