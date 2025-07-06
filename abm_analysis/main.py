import os
import sys

import llm

import thematic_analysis
import thematic_analysis_evaluation
import thematic_analysis_extra
import key_component_generation

import profile_generation
import profile_evaluation as profile_evaluation
import scenario_decision
import scenario_decision_evaluation
import decision_table
import script_generation


def get_transcript_file_paths(source_path):
    return ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    # return [f"{source_path}/{filename}" for filename in sorted(os.listdir(source_path))]


def main(objective, model_input, model_output, questions):
    source_paths = get_transcript_file_paths("data/diary_txt")
    results_path = "abm_analysis/results"
    os.makedirs(results_path, exist_ok=True)

    step = int(
        input(
            """Steps:
1 - Generate EABSS Key components (scope, diagrams)
2 - Generate Profiles and action probability table
3 - Generate Simulation script (NetLogo)

Select step: """
        )
    )

    ta_codes_txt_path = results_path + "/thematic_analysis_codes.txt"
    ta_codes_csv_path = results_path + "/thematic_analysis_codes.csv"

    if step == 1:
        # Extract key components codes with supporting quotes
        thematic_analysis.analyse(source_paths, ta_codes_txt_path, ta_codes_csv_path)
        thematic_analysis_evaluation.evaluate(ta_codes_csv_path)
        thematic_analysis_extra.analyse(source_paths)

        kc_scope_path = results_path + "/key_component_scope.txt"
        kc_usecase_diagram_path = results_path + "/key_component_usecase_diagram.txt"
        kc_activity_diagram_path = results_path + "/key_component_activity_diagram.txt"
        kc_state_transition_diagram_path = (
            results_path + "/key_component_state_transition_diagram.txt"
        )
        kc_interaction_diagram_path = (
            results_path + "/key_component_interaction_diagram.txt"
        )

        # Generate ABM key components
        key_component_generation.generate(
            objective,
            model_input,
            model_output,
            ta_codes_txt_path,
            kc_scope_path,
            kc_usecase_diagram_path,
            kc_activity_diagram_path,
            kc_state_transition_diagram_path,
            kc_interaction_diagram_path,
        )

        # + human review: codes and quotes coherence, diagrams review
        print("- Done -")
        print(
            """Please review generated results and update "Archetype model" and "Scenario questions\""""
        )

    profiles_path = results_path + "/profiles.txt"

    if step == 2:
        pass
        # Profiles generation
        profile_generation.generate(
            source_paths,
            objective,
            kc_scope_path,
            profiles_path,
        )
        profile_evaluation.evaluate(profiles_path)
        # + human review: attribute correctness and archetype and quotes coherence

    scenario_questions_path = results_path + "/scenario_questions.txt"
    scenario_ground_truth_path = results_path + "/scenario_ground_truth.txt"

    scenario_answers_path = results_path + "/scenario_answers.csv"
    scenario_scores_path = results_path + "/scenario_scores.csv"

    if step == 2:
        pass
        # Scenario-question create
        with open(scenario_questions_path, "w") as f:
            f.write(questions)

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

    scenario_probability_path = results_path + "/scenario_probability.csv"

    if step == 2:
        pass
        # Decision table
        decision_table.generate(
            scenario_questions_path, scenario_answers_path, scenario_probability_path
        )

        print("- Done -")

    simulation_script_path = results_path + "/simulation_script.txt"

    if step == 3:
        # Generate simulation script
        script_generation.generate(
            objective,
            model_input,
            model_output,
            kc_scope_path,
            kc_usecase_diagram_path,
            kc_activity_diagram_path,
            kc_state_transition_diagram_path,
            kc_interaction_diagram_path,
            scenario_probability_path,
            simulation_script_path,
        )

        print("- Done -")
        print(
            """Please review generated script. Further edit might required (ChatGPT can help fix the script)"""
        )


if __name__ == "__main__":
    # Objective, Input, Output
    objective = "explore different usages of transportation from home to workplace"
    model_input = "traveller characteristic (transportation preference)"
    model_output = "number of used of each transportation type"

    questions = """[
"Which transport mode do you usually take?",
"Which transport mode do you take when it rain?"
]"""

    main(objective, model_input, model_output, questions)
