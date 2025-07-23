import os
import sys

import stage_01_objective_setup
import stage_02_build_eabss
import stage_03_generate_eabss_diagram
import stage_04_archetype_scenario_setup
import stage_05_profile_generation
import stage_06_scenario_decision
import stage_07_script_generation

import display_progress
import paths


# TODO: resume the process: error at profile 3 > should continue at profile 4
# TODO: add comments


def get_transcript_file_paths(source_path):
    # return ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    return [
        f"{source_path}/{filename}" for filename in sorted(os.listdir(source_path))[0:5]
    ]


def ask_proceed(stage_str: str) -> bool:
    approve = None
    while approve not in ["y", "n"]:
        approve = input(f"\nProceed to next stage: {stage_str}? (y/n): ").lower()
    return approve == "y"


def print_end_stage(is_last_stage: bool = False):
    if not is_last_stage:
        print("\nRun 'main.py' to continue to the next stage.\n")
    else:
        print("-" * 50 + "\nAll model development stages completed\n" + "=" * 50)
        print("\nRun 'main_post.py' to analyse the model output.\n")


def main(source_folder: str, results_folder: str):
    source_paths = get_transcript_file_paths(source_folder)
    results_path = results_folder
    os.makedirs(results_path, exist_ok=True)

    # NOTE: if main file of that stage exists that process already done
    # eg. if not os.path.isfile(stage_result_file.txt):

    ## Define Objective, Input, Output
    objective_statement_path = os.path.join(results_path, paths.objective_file_path)

    if not os.path.isfile(objective_statement_path):
        # New project
        print("\nNo existing project detected.")
        print("Starting new project...")
        stage_01_objective_setup.define_objective_statement(objective_statement_path)

        print(display_progress.objective_statement_progress(objective_statement_path))

        print_end_stage()
        sys.exit()
    else:
        # Display objective result
        display_progress.display_header()
        print(display_progress.objective_statement_progress(objective_statement_path))

    ## Build EABSS components
    ta_codes_txt_path = os.path.join(results_path, paths.thematic_codes_file_path)
    eabss_components_path = os.path.join(results_path, paths.eabss_scope_file_path)

    if not os.path.isfile(eabss_components_path):
        stage_str = "Build EABSS components"
        proceed = ask_proceed(stage_str)

        if proceed:
            # Thematic analysis
            stage_02_build_eabss.analyse(
                source_paths,
                ta_codes_txt_path,
            )

            # Finalise EABSS components
            stage_02_build_eabss.generate_final_components(
                objective_statement_path,
                ta_codes_txt_path,
                eabss_components_path,
            )

            print()
            print(display_progress.eabss_components_progress(eabss_components_path))

            print_end_stage()

        sys.exit()
    else:
        # Display EABSS components result
        print(display_progress.eabss_components_progress(eabss_components_path))

    ## Build EABSS diagrams
    eabss_usecase_diagram_path = os.path.join(
        results_path, paths.eabss_usecase_file_path
    )

    eabss_class_diagram_path = os.path.join(results_path, paths.eabss_class_file_path)
    eabss_activity_diagram_path = os.path.join(
        results_path, paths.eabss_activity_file_path
    )
    eabss_state_transition_diagram_path = os.path.join(
        results_path, paths.eabss_state_file_path
    )
    # TODO: (optional) add transition table
    # eabss_state_transition_table_path = os.path.join(results_path,"eabss_diagram_state_table.txt")
    eabss_interaction_diagram_path = os.path.join(
        results_path, paths.eabss_interaction_file_path
    )

    if not os.path.isfile(eabss_usecase_diagram_path):
        stage_str = "Generate EABSS diagrams - use case diagram"
        proceed = ask_proceed(stage_str)
        if proceed:
            # Generate EABSS usecase diagrams
            stage_03_generate_eabss_diagram.generate_usecase_diagrams(
                eabss_components_path,
                eabss_usecase_diagram_path,
            )

            print(display_progress.diagram_header())
            print(
                display_progress.eabss_usecase_diagrams_progess(
                    eabss_usecase_diagram_path,
                )
            )

            print_end_stage()
        sys.exit()
    else:
        # Display EABSS usecase diagrams result
        print(display_progress.diagram_header())
        print(
            display_progress.eabss_usecase_diagrams_progess(
                eabss_usecase_diagram_path,
            )
        )

    if (
        not os.path.isfile(eabss_activity_diagram_path)
        or not os.path.isfile(eabss_state_transition_diagram_path)
        or not os.path.isfile(eabss_interaction_diagram_path)
        or not os.path.isfile(eabss_class_diagram_path)
    ):
        stage_str = "Generate EABSS diagrams - remaining diagrams"
        proceed = ask_proceed(stage_str)
        if proceed:
            # Generate EABSS diagrams
            stage_03_generate_eabss_diagram.generate_diagrams(
                eabss_components_path,
                eabss_usecase_diagram_path,
                eabss_activity_diagram_path,
                eabss_state_transition_diagram_path,
                eabss_interaction_diagram_path,
                eabss_class_diagram_path,
            )

            print(display_progress.diagram_header())
            print(
                display_progress.eabss_diagrams_progess(
                    eabss_activity_diagram_path,
                    eabss_state_transition_diagram_path,
                    eabss_interaction_diagram_path,
                    eabss_class_diagram_path,
                )
            )

            print_end_stage()
        sys.exit()
    else:
        # Display EABSS remaining diagrams result
        print(
            display_progress.eabss_diagrams_progess(
                eabss_activity_diagram_path,
                eabss_state_transition_diagram_path,
                eabss_interaction_diagram_path,
                eabss_class_diagram_path,
            )
        )

    ## Define archetyp, scenario questions, scenarion answer choices
    archetype_path = os.path.join(results_path, paths.archetype_file_path)
    attribute_path = os.path.join(results_path, paths.attribute_file_path)
    scenario_questions_path = os.path.join(
        results_path, paths.scenario_questions_file_path
    )
    scenario_choices_path = os.path.join(results_path, paths.scenario_choices_file_path)

    if (
        not os.path.isfile(archetype_path)
        or not os.path.isfile(attribute_path)
        or not os.path.isfile(scenario_questions_path)
        or not os.path.isfile(scenario_choices_path)
    ):
        stage_str = (
            "Define Archetype, Profile attribute, Scenario questions & answer choices"
        )
        proceed = ask_proceed(stage_str)
        if proceed:
            # Define archetyp, scenario questions, scenarion answer choices
            stage_04_archetype_scenario_setup.setup_archetype_attribute_scenario(
                eabss_components_path,
                archetype_path,
                attribute_path,
                scenario_questions_path,
                scenario_choices_path,
            )

            # Generate ground truth
            stage_04_archetype_scenario_setup.create_ground_truth(
                scenario_questions_path,
                scenario_ground_truth_path,
            )

            print(display_progress.archetype_progess(archetype_path))
            print(display_progress.attribute_progess(attribute_path))
            print(
                display_progress.scenario_progess(
                    scenario_questions_path,
                    scenario_choices_path,
                )
            )
            print(
                display_progress.ground_truth_progess(
                    scenario_questions_path, archetype_path, scenario_ground_truth_path
                )
            )

            print_end_stage()
        sys.exit()
    else:
        # Display Archetype, Scenario questions & answer choices
        print(display_progress.archetype_progess(archetype_path))
        print(display_progress.attribute_progess(attribute_path))
        print(
            display_progress.scenario_progess(
                scenario_questions_path,
                scenario_choices_path,
            )
        )
        print(
            display_progress.ground_truth_progess(
                scenario_questions_path, archetype_path, scenario_ground_truth_path
            )
        )

    ## Extract Profiles (& classify profile archetype)
    profiles_path = os.path.join(results_path, paths.profile_file_path)

    if not os.path.isfile(profiles_path):
        stage_str = "Extract profiles"
        proceed = ask_proceed(stage_str)
        if proceed:
            # Extract profile
            stage_05_profile_generation.generate(
                source_paths,
                objective_statement_path,
                eabss_components_path,
                attribute_path,
                profiles_path,
            )

            print(display_progress.profile_progess(profiles_path))

            print_end_stage()
        sys.exit()
    else:
        # Display Profiles saved location
        print(display_progress.profile_progess(profiles_path))

    ## Create Decision probability table
    profile_scenario_answers_path = os.path.join(
        results_path, paths.profile_scenario_answers_file_path
    )
    decision_probability_path = os.path.join(
        results_path, paths.scenario_probability_file_path
    )

    if not os.path.isfile(decision_probability_path):
        stage_str = "Decision probability table"
        proceed = ask_proceed(stage_str)
        if proceed:
            # # Answer scenario-questions
            if not os.path.isfile(profile_scenario_answers_path):
                stage_06_scenario_decision.generate_profile_scenario_answers(
                    scenario_questions_path,
                    profiles_path,
                    profile_scenario_answers_path,
                )

                # Display scenario question' answer of each profile
                print(
                    display_progress.profile_scenario_answer_progess(
                        profile_scenario_answers_path
                    )
                )

            # Create decision probability table
            stage_06_scenario_decision.generate_decision_prob_table(
                scenario_questions_path,
                profile_scenario_answers_path,
                decision_probability_path,
            )

            print(
                display_progress.decision_probability_table_progess(
                    decision_probability_path
                )
            )

            print_end_stage()
        sys.exit()
    else:
        # Display Scenario answer saved path & Decision probability table
        print(
            display_progress.profile_scenario_answer_progess(
                profile_scenario_answers_path
            )
        )
        print(
            display_progress.decision_probability_table_progess(
                decision_probability_path
            )
        )

    ## Generate Simulation script
    simulation_script_think_path = os.path.join(
        results_path, paths.simulation_script_think_file_path
    )
    simulation_script_path = os.path.join(
        results_path, paths.simulation_script_file_path
    )

    if not os.path.isfile(simulation_script_path):
        stage_str = "Generate simulation script"
        proceed = ask_proceed(stage_str)
        if proceed:
            stage_07_script_generation.generate(
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
            )

            print(
                display_progress.profile_scenario_answer_progess(simulation_script_path)
            )
            print_end_stage(True)
        sys.exit()
    else:
        print(display_progress.profile_scenario_answer_progess(simulation_script_path))
        print_end_stage(True)

    print()


if __name__ == "__main__":
    source_folder = "data/diary_txt"
    results_folder = "results_4"
    # TODO: pick source & project from terminal (optional)
    main(source_folder, results_folder)
