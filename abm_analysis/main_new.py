import os
import sys
import json

import problem_statement_definition

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

import display_progress


def get_transcript_file_paths(source_path):
    return ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    # return [f"{source_path}/{filename}" for filename in sorted(os.listdir(source_path))]


def main_0(objective, model_input, model_output, questions):
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


def main(source_folder: str, results_folder: str):
    source_paths = get_transcript_file_paths(source_folder)
    results_path = results_folder
    os.makedirs(results_path, exist_ok=True)

    ## Define Problem statement, Input * Ouput
    problem_statement_path = results_path + "/problem_statement.txt"
    # TODO: state problem

    ## Build EABSS components
    # Thematic analysis
    ta_codes_txt_path = results_path + "/thematic_analysis_codes.txt"
    # TODO: conduct thematic analyse

    # Finalise EABSS
    EABSS_components_path = results_path + "/eabss_scope.txt"
    EABSS_usecase_diagram_path = results_path + "/eabss_diagram.txt"
    EABSS_activity_diagram_path = results_path + "/eabss_activity_diagram.txt"
    EABSS_state_transition_diagram_path = results_path + "/eabss_state_diagram.txt"
    # TODO: add transition table = results_path + "/eabss_state_table.txt"
    EABSS_interaction_diagram_path = results_path + "/eabss_interaction_diagram.txt"
    # TODO: finalise EABSS components
    # TODO: tell user to review & update EABSS components
    # TODO: tell user to update relevant models for next step (archetypes, questions, choices)

    ## Define scenario-questions & answer choices
    # Define scenario questions
    # TODO:
    # Define scenario answer choices
    # TODO:

    ## Extract Profiles (& classify profile archetype)
    # Extract profile
    profiles_path = results_path + "/profiles.txt"
    # TODO:

    # Answer scenario-questions
    scenario_questions_path = results_path + "/scenario_questions.txt"
    scenario_answers_path = results_path + "/scenario_answers.csv"
    # TODO:

    # # Profile Evaluation
    # scenario_ground_truth_path = results_path + "/scenario_ground_truth.txt"
    # scenario_scores_path = results_path + "/scenario_scores.csv"
    # # TODO: extract profiles

    ## Create Decision probability table
    decision_probability_path = results_path + "/scenario_probability.csv"
    # TODO: create table

    ## Generate Simulation script
    simulation_script_path = results_path + "/simulation_script.txt"
    # TODO: generate simulation script
    # TODO: tell user to review & update script (manually/LLMs)

    # //

    # NOTE: if main file of that stage exists that process already done
    # if not os.path.isfile(problem_statement_path):
    # TODO: (optional) change to check project name and its stage in json
    if not os.path.isfile(problem_statement_path):
        print("\nNo existing project detected.")
        print("Starting new project...")
        problem_statement_definition.define_problem_statement(problem_statement_path)
        print("Stage 1 complete.")
        print("Please run 'python main.py' to continue to the next step.")
        sys.exit()

    if not os.path.isfile(EABSS_components_path):
        display_progress.display(problem_statement_path)

        # TODO: implement build eabss
        print("Stage 2 complete.")
        sys.exit()

    if not os.path.isfile(scenario_questions_path) and not os.path.isfile(
        scenario_answers_path
    ):
        print("- scenario questions step")
        # TODO: back to complete previous step or continue
        # TODO: remind update scenario questions & answers
        pass
        sys.exit()
    if not os.path.isfile(profiles_path):
        print("- extract profiles step")
        # TODO: back to complete previous step or continue
        # TODO: implement extract profile
        pass
    if not os.path.isfile(decision_probability_path):
        print("- decision prob step")
        # TODO: implement create decision table
        pass
    if not os.path.isfile(simulation_script_path):
        print("- sim script step")
        # TODO: implement generate script
        pass

    print("- Done -")
    sys.exit()


if __name__ == "__main__":
    source_folder = "data/diary_txt"
    results_folder = "abm_analysis/results_1"
    # TODO: pick project
    main(source_folder, results_folder)
