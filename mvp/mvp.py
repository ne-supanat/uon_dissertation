import os

import llm

import thematic_analysis
import thematic_analysis_evaluation
import key_component_generation

import profile_generation
import profile_generation_evaluation
import scenario_decision
import scenario_decision_evaluation
import decision_table


def get_objective():
    return "explore sustainability in different usages of transportation from home to workplace"


def get_input_output():
    return (
        "traveller characteristic (age, gender, occupation, transportation preference)",
        "number of used of each transportation type",
    )


def generate_simulation_script(
    obj, input, output, key_component, usecase, activity, state_transition, action_prob
):
    prompt = f"""
Based on these EABSS key components

{key_component}

Objective
{obj}

Input
{input}

Output
{output}

UML use case diagram
{usecase}

UML activity diagram
{activity}

UML state transition diagram
{state_transition}

Archetype action probability
{action_prob}

generate agentPy simulation script
"""
    response = llm.generate_content(prompt)
    return response.text


def main():
    os.makedirs("mvp/results", exist_ok=True)

    # Objective
    objective = "explore different usages of transportation from home to workplace"

    # Input, Output
    input, output = get_input_output()

    document_paths = ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]

    ta_codes_txt_path = "mvp/results/thematic_analysis_codes.txt"
    ta_codes_csv_path = "mvp/results/thematic_analysis_codes.csv"

    # Extract key components codes with supporting quotes
    thematic_analysis.analyse(document_paths, ta_codes_txt_path, ta_codes_csv_path)
    thematic_analysis_evaluation.evaluate(document_paths)

    kc_scope_path = "mvp/results/key_component_scope.txt"
    kc_usecase_diagram_path = "mvp/results/key_component_usecase_diagram.txt"
    kc_activity_diagram_path = "mvp/results/key_component_activity_diagram.txt"
    kc_state_transition_diagram_path = (
        "mvp/results/key_component_state_transition_diagram.txt"
    )

    # Generate ABM key components
    key_component_generation.generate(
        objective,
        input,
        output,
        ta_codes_txt_path,
        kc_scope_path,
        kc_usecase_diagram_path,
        kc_activity_diagram_path,
        kc_state_transition_diagram_path,
    )
    # + human review: codes and quotes coherence, diagrams review

    profiles_path = "mvp/results/profiles.txt"

    # Profiles generation
    profile_generation.generate(
        document_paths,
        objective,
        kc_scope_path,
        profiles_path,
    )
    profile_generation_evaluation.evaluate(profiles_path)
    # + human review: attribute correctness and archetype and quotes coherence

    scenario_questions_path = "mvp/results/scenario_questions.txt"
    scenario_ground_truth_path = "mvp/results/scenario_ground_truth.txt"

    scenario_answers_path = "mvp/results/scenario_answers.csv"
    scenario_scores_path = "mvp/results/scenario_scores.csv"

    # Scenario-question answering
    scenario_decision.generate_profile_answers(
        scenario_questions_path,
        profiles_path,
        scenario_answers_path,
    )
    scenario_decision_evaluation.generate_ground_truth(
        scenario_questions_path,
        scenario_ground_truth_path,
    )
    scenario_decision_evaluation.score_profile_anwsers(
        scenario_ground_truth_path,
        scenario_answers_path,
        scenario_scores_path,
    )

    scenario_probability_path = "scenario_probability.csv"

    # Decision table
    decision_table.generate(scenario_questions_path, scenario_probability_path)

    # # Generate simulation script
    # with open(f"mvp/results/usecase_diagram.txt", "r") as f:
    #     usecase = f.read()

    # with open(f"mvp/results/activity_diagram.txt", "r") as f:
    #     activity = f.read()

    # with open(f"mvp/results/state_transition_diagram.txt", "r") as f:
    #     stateTransition = f.read()

    # with open(f"mvp/results/answer_prob.csv", "r") as f:
    #     actionProb = f.read()

    # script = generateSimulationScript(
    #     obj,
    #     input,
    #     output,
    #     keyComponents,
    #     usecase,
    #     activity,
    #     stateTransition,
    #     actionProb,
    # )
    # with open(f"mvp/results/script.py", "w") as f:
    #     f.write(script)


if __name__ == "__main__":
    main()
