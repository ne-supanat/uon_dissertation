import os

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


def main():
    os.makedirs("abm_analysis/results", exist_ok=True)

    # Objective, Input, Output
    objective = "explore different usages of transportation from home to workplace"
    input = "traveller characteristic (transportation preference)"
    output = "number of used of each transportation type"

    document_paths = get_transcript_file_paths("data/diary_txt")

    ta_codes_txt_path = "abm_analysis/results/thematic_analysis_codes.txt"
    ta_codes_csv_path = "abm_analysis/results/thematic_analysis_codes.csv"

    # # Extract key components codes with supporting quotes
    # thematic_analysis.analyse(document_paths, ta_codes_txt_path, ta_codes_csv_path)
    # thematic_analysis_evaluation.evaluate(ta_codes_csv_path)
    # thematic_analysis_extra.analyse(document_paths)

    kc_scope_path = "abm_analysis/results/key_component_scope.txt"
    kc_usecase_diagram_path = "abm_analysis/results/key_component_usecase_diagram.txt"
    kc_activity_diagram_path = "abm_analysis/results/key_component_activity_diagram.txt"
    kc_state_transition_diagram_path = (
        "abm_analysis/results/key_component_state_transition_diagram.txt"
    )

    # # Generate ABM key components
    # key_component_generation.generate(
    #     objective,
    #     input,
    #     output,
    #     ta_codes_txt_path,
    #     kc_scope_path,
    #     kc_usecase_diagram_path,
    #     kc_activity_diagram_path,
    #     kc_state_transition_diagram_path,
    # )
    # # + human review: codes and quotes coherence, diagrams review
    # # * UPDATE archetype model *

    profiles_path = "abm_analysis/results/profiles.txt"

    # # Profiles generation
    # profile_generation.generate(
    #     document_paths,
    #     objective,
    #     kc_scope_path,
    #     profiles_path,
    # )
    # profile_evaluation.evaluate(profiles_path)
    # # + human review: attribute correctness and archetype and quotes coherence

    scenario_questions_path = "abm_analysis/results/scenario_questions.txt"
    scenario_ground_truth_path = "abm_analysis/results/scenario_ground_truth.txt"

    scenario_answers_path = "abm_analysis/results/scenario_answers.csv"
    scenario_scores_path = "abm_analysis/results/scenario_scores.csv"

    # Scenario-question create
    with open(scenario_questions_path, "w") as f:
        f.write(
            """[
"Which transport mode do you usually take?",
"Which transport mode do you take when it rain?"
]"""
        )

    # # Scenario-question answering
    # scenario_decision.generate_profile_answers(
    #     scenario_questions_path,
    #     profiles_path,
    #     scenario_answers_path,
    # )
    # scenario_decision_evaluation.generate_ground_truth(
    #     scenario_questions_path,
    #     scenario_ground_truth_path,
    # )
    # scenario_decision_evaluation.score_profile_anwsers(
    #     scenario_ground_truth_path,
    #     scenario_answers_path,
    #     scenario_scores_path,
    # )

    scenario_probability_path = "abm_analysis/results/scenario_probability.csv"

    # # Decision table
    # decision_table.generate(
    #     scenario_questions_path, scenario_answers_path, scenario_probability_path
    # )

    simulation_script_path = "abm_analysis/results/simulation_script.txt"

    # # Generate simulation script
    # script_generation.generate(
    #     objective,
    #     input,
    #     output,
    #     kc_scope_path,
    #     kc_usecase_diagram_path,
    #     kc_activity_diagram_path,
    #     kc_state_transition_diagram_path,
    #     scenario_probability_path,
    #     simulation_script_path,
    # )


if __name__ == "__main__":
    main()
