import os
import sys
import json

import objective_setup

import thematic_analysis
import thematic_analysis_evaluation
import thematic_analysis_extra
import key_component_generation

import archetype_scenario_setup

import profile_generation
import profile_evaluation
import scenario_decision
import scenario_decision_evaluation
import decision_table
import script_generation

import display_progress


def get_transcript_file_paths(source_path):
    return ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    # return [f"{source_path}/{filename}" for filename in sorted(os.listdir(source_path))]


def ask_approval(stage_str: str) -> bool:
    approve = None
    while approve not in ["y", "n"]:
        approve = input(f"\nProceed to next stage: {stage_str}? (y/n): ").lower()
    return approve == "y"


def print_end_stage(is_last_stage: bool = False):
    if not is_last_stage:
        print("\nRun 'python main.py' to continue to the next stage.\n")
    else:
        print("\n- Done -\n")


def main(source_folder: str, results_folder: str):
    source_paths = get_transcript_file_paths(source_folder)
    results_path = results_folder
    os.makedirs(results_path, exist_ok=True)

    # NOTE: if main file of that stage exists that process already done
    # if not os.path.isfile(problem_statement_path):
    # TODO: (optional) change to check project name and its stage in json
    # TODO: make user approve the stage result first

    ## Define Objective, Input, Output
    problem_statement_path = os.path.join(results_path, "objective.txt")

    if not os.path.isfile(problem_statement_path):
        # New project
        print("\nNo existing project detected.")
        print("Starting new project...")
        objective_setup.define_problem_statement(problem_statement_path)
        display_progress.display_problem_statement(problem_statement_path)
        print_end_stage()
        sys.exit()
    else:
        # Display objective result
        display_progress.display_header()
        display_progress.display_problem_statement(problem_statement_path)

    ## Build EABSS components
    ta_codes_txt_path = os.path.join(results_path, "thematic_analysis_codes.txt")
    ta_codes_csv_path = os.path.join(results_path, "thematic_analysis_codes.csv")

    eabss_components_path = os.path.join(results_path, "eabss_scope.txt")

    if not os.path.isfile(eabss_components_path):
        stage_str = "Build EABSS components"
        proceed = ask_approval(stage_str)

        if proceed:
            # Thematic analysis
            thematic_analysis.analyse(
                source_paths,
                ta_codes_txt_path,
                ta_codes_csv_path,
            )

            # Finalise EABSS components
            key_component_generation.generate_components(
                problem_statement_path,
                ta_codes_txt_path,
                eabss_components_path,
            )

            # # EABSS components Evaluation
            # thematic_analysis_evaluation.evaluate(ta_codes_csv_path)
            # thematic_analysis_extra.analyse(source_paths)

            print()
            display_progress.display_eabss_components(eabss_components_path)
            print_end_stage()

        sys.exit()
    else:
        # Display EABSS components result
        display_progress.display_eabss_components(eabss_components_path)

    ## Build EABSS diagrams
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

    if not os.path.isfile(eabss_usecase_diagram_path):
        stage_str = "Generate EABSS diagrams"
        proceed = ask_approval(stage_str)
        if proceed:
            # Generate EABSS diagrams
            key_component_generation.generate_diagrams(
                eabss_components_path,
                eabss_usecase_diagram_path,
                eabss_activity_diagram_path,
                eabss_state_transition_diagram_path,
                eabss_interaction_diagram_path,
            )

            display_progress.display_eabss_diagrams(
                eabss_usecase_diagram_path,
                eabss_activity_diagram_path,
                eabss_state_transition_diagram_path,
                eabss_interaction_diagram_path,
            )

            print_end_stage()
        sys.exit()
    else:
        # Display EABSS diagrams result
        display_progress.display_eabss_diagrams(
            eabss_usecase_diagram_path,
            eabss_activity_diagram_path,
            eabss_state_transition_diagram_path,
            eabss_interaction_diagram_path,
        )

    # ## Define scenario-questions & answer choices
    # archetype_path = os.path.join(results_path, "archetype.py")
    # scenario_questions_path = os.path.join(results_path, "scenario_questions.txt")
    # scenario_answer_choices_path = os.path.join(results_path, "answers_choices.py")

    # if (
    #     not os.path.isfile(archetype_path)
    #     or not os.path.isfile(scenario_questions_path)
    #     or not os.path.isfile(scenario_answer_choices_path)
    # ):
    #     stage_str = "Define Archetype, Scenario questions & answer choices"
    #     proceed = ask_approval(stage_str)
    #     archetype_scenario_setup.setup_archetype_scenario()
    #     # TODO: tell user to update relevant models for next step (archetypes, questions, choices)
    #     print("- scenario questions step")
    #     # Define scenario questions
    #     # TODO:
    #     # with open(scenario_questions_path, "w") as f:
    #     #     f.write("questions")
    #     # Define scenario answer choices
    #     # TODO:

    #     print_end_stage(stage_str)
    #     sys.exit()

    # ## Extract Profiles (& classify profile archetype)
    # profiles_path = os.path.join(results_path, "profiles.txt")
    # scenario_answers_path = os.path.join(results_path, "scenario_answers.csv")

    # if not os.path.isfile(profiles_path):
    #     print("- extract profiles step")
    #     # Extract profile
    #     profile_generation.generate(
    #         source_paths,
    #         problem_statement_path,
    #         eabss_components_path,
    #         profiles_path,
    #     )
    #     # Answer scenario-questions
    #     scenario_decision.generate_profile_answers(
    #         scenario_questions_path,
    #         profiles_path,
    #         scenario_answers_path,
    #     )
    #     # # Profile Evaluation
    #     # scenario_ground_truth_path = os.path.join(results_path, "scenario_ground_truth.txt")
    #     # scenario_scores_path = os.path.join(results_path, "scenario_scores.csv")
    #     # profile_evaluation.evaluate(profiles_path)
    #     # scenario_decision_evaluation.generate_ground_truth(
    #     #     scenario_questions_path,
    #     #     scenario_ground_truth_path,
    #     # )
    #     # scenario_decision_evaluation.score_profile_anwsers(
    #     #     scenario_ground_truth_path,
    #     #     scenario_answers_path,
    #     #     scenario_scores_path,
    #     # )

    #     print_end_stage(4)
    #     sys.exit()

    # ## Create Decision probability table
    # decision_probability_path = os.path.join(results_path, "scenario_probability.csv")
    # if not os.path.isfile(decision_probability_path):
    #     print("- decision prob step")
    #     decision_table.generate(
    #         scenario_questions_path, scenario_answers_path, decision_probability_path
    #     )
    #     print_end_stage(5)
    #     sys.exit()

    # ## Generate Simulation script
    # simulation_script_path = os.path.join(results_path, "simulation_script.txt")

    # if not os.path.isfile(simulation_script_path):
    #     print("- sim script step")
    #     script_generation.generate(
    #         problem_statement_path,
    #         eabss_components_path,
    #         eabss_usecase_diagram_path,
    #         eabss_activity_diagram_path,
    #         eabss_state_transition_diagram_path,
    #         eabss_interaction_diagram_path,
    #         decision_probability_path,
    #         simulation_script_path,
    #     )
    #     # TODO: tell user to review & update script (manually/LLMs)

    #     print_end_stage(6)
    #     sys.exit()
    print()


if __name__ == "__main__":
    source_folder = "data/diary_txt"
    results_folder = "abm_analysis/results_2"
    # TODO: pick project
    main(source_folder, results_folder)
