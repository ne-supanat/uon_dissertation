import argparse
import os
import sys

import stage_00_project_setup
import stage_01_objective_setup
import stage_02_build_eabss
import stage_03_generate_eabss_diagram
import stage_04_archetype_scenario_setup
import stage_05_profile_extraction
import stage_06_scenario_decision
import stage_07_script_generation

import display_progress
from system_path import SystemPath


# TODO: resume the process: error at profile 3 > should continue at profile 4
# TODO: add comments
# TODO: criteria table


def get_transcript_file_paths(source_directory):
    return [
        f"{os.path.join(source_directory, filename)}"
        for filename in sorted(os.listdir(source_directory))
        if filename.endswith(".txt")
    ][
        :  # TODO: change back to all docs
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
        print("\nRun 'main.py' to review the progress.")
        print("Run 'main_post.py' to analyse the model output.")
        print("Run 'main_eval.py' to evaluate the system outputs.")


def run_setup_project(path: SystemPath):
    if not os.path.isdir(path.project_name):
        # Start new project
        print("\nNo existing project detected.")
        print("Starting new project...")

        stage_00_project_setup.run_setup_project(path)
    else:
        display_progress.display_header()


def run_setup_topic_outline(path: SystemPath):
    if not os.path.isfile(path.get_01_topic_path()) or not os.path.isfile(
        path.get_01_outline_path()
    ):
        # Setup topic and outline of the model
        stage_01_objective_setup.setup_topic(path)
        print()
        stage_01_objective_setup.setup_outline(path)

        # Display topic & outline of the model
        print(display_progress.topic_outline_progress(path))

        print_end_stage()
        sys.exit()
    else:
        # Display topic & outline of the model
        print(display_progress.topic_outline_progress(path))


def run_build_eabss(path: SystemPath):
    if not os.path.isfile(path.get_02_eabss_scope_path()):
        stage_str = "Build EABSS components"
        proceed = ask_proceed(stage_str)

        if proceed:
            # Thematic analysis
            scope_document_paths = get_transcript_file_paths(
                path.get_scope_data_directory_path()
            )
            stage_02_build_eabss.run_thematic_analysis(path, scope_document_paths)
            print()

            # Finalise EABSS components
            stage_02_build_eabss.run_eabss_scope_finalisation(path)

            # Display EABSS components result
            print(display_progress.eabss_scope_progress(path))
            print_end_stage()

        sys.exit()
    else:
        # Display EABSS components result
        print(display_progress.eabss_scope_progress(path))


def run_build_eabss_usecase_diagramm(path: SystemPath):
    if not os.path.isfile(path.get_03_eabss_usecase_diagram_path()):
        stage_str = "Generate EABSS diagrams - use case diagram"
        proceed = ask_proceed(stage_str)
        if proceed:
            # Generate EABSS usecase diagrams
            stage_03_generate_eabss_diagram.build_eabss_usecase_diagrams(path)

            print_end_stage()
        sys.exit()
    else:
        # Display EABSS usecase diagrams result
        print(display_progress.diagram_header())
        print(display_progress.eabss_usecase_diagrams_progess(path))


def should_build_remaining_eabss_diagrams(path: SystemPath):
    # Check if any of remaining diagram result files does not exist.
    return (
        not os.path.isfile(path.get_03_eabss_activity_diagram_path())
        or not os.path.isfile(path.get_03_eabss_state_diagram_path())
        or not os.path.isfile(path.get_03_eabss_interaction_diagram_path())
        or not os.path.isfile(path.get_03_eabss_class_diagram_path())
    )


def run_build_remaining_eabss_diagrams(path: SystemPath):
    if should_build_remaining_eabss_diagrams(path):
        stage_str = "Generate EABSS diagrams - remaining diagrams"
        proceed = ask_proceed(stage_str)
        if proceed:
            # Generate EABSS diagrams
            stage_03_generate_eabss_diagram.buidl_eabss_remaining_diagrams(path)

            print_end_stage()
        sys.exit()
    else:
        # Display EABSS remaining diagrams result
        print(display_progress.eabss_diagrams_progess(path))


def should_design_profile_n_scenario(path: SystemPath):
    # Check if any of result files of design and profile step does not exist.
    return (
        not os.path.isfile(path.get_04_archetypes_path())
        or not os.path.isfile(path.get_04_attributes_path())
        or not os.path.isfile(path.get_04_scenario_questions_path())
        or not os.path.isfile(path.get_04_scenario_choices_path())
    )


def run_design_profile_n_scenario(path: SystemPath):
    if should_design_profile_n_scenario(path):
        stage_str = "Design Profile and Scenario"
        proceed = ask_proceed(stage_str)
        if proceed:
            # Design profile & scenarion
            stage_04_archetype_scenario_setup.design_profile_n_scenario(path)

            display_progress.display_stage04(path)
            print_end_stage()
        sys.exit()
    else:
        # Display Archetype, Attributes, Scenario questions, Scenario answer choices saved locations
        display_progress.display_stage04(path)


def run_extract_profiles(path: SystemPath):
    if not os.path.isfile(path.get_05_profiles_path()):
        stage_str = "Extract profiles"
        proceed = ask_proceed(stage_str)
        if proceed:
            # Extract profile
            profile_document_paths = get_transcript_file_paths(
                path.get_profile_data_directory_path()
            )
            stage_05_profile_extraction.extract_profile(path, profile_document_paths)

            print_end_stage()
        sys.exit()
    else:
        # Display Profiles saved location
        print(display_progress.profile_progess(path))


def run_create_decision_probability_table(path: SystemPath):
    if not os.path.isfile(path.get_06_decision_probability_path()):
        stage_str = "Decision probability table"
        proceed = ask_proceed(stage_str)
        if proceed:
            # Create ground truth
            if not os.path.isfile(path.get_06_scenario_ground_truth_path()):
                stage_06_scenario_decision.create_ground_truth(path)

            print(display_progress.ground_truth_progess(path))

            # Ask user to use extracted profiles or generated ground truth
            # to create scenario answers
            with open(path.get_04_scenario_questions_path(), "r") as f:
                questions = f.read().strip().splitlines()

            with open(path.get_05_profiles_path(), "r") as f:
                content = f.read()
            profiles = [profile for profile in content.strip().split("\n\n")]
            profile_size = len(profiles)

            print()
            print(
                f"Select the method to answer the scenario question{"s" if len(questions) > 1 else ""}"
            )
            profile_str = "profile" + "s" if profile_size > 1 else ""
            print(
                f"1. Use {profile_str} based on extracted {profile_str} ({profile_size} result{"s" if profile_size>1 else ""})"
            )
            print(f"2. Use profiles based on ground truth ({100} results)")

            method = None
            while method not in ["1", "2"]:
                method = input(f"\nEnter the method number (1 or 2): ").lower()

            # Answer scenario questions
            if method == "1":
                # Based on extracted profile(s)
                stage_06_scenario_decision.create_profile_scenario_answers(path)
            elif method == "2":
                # Based on ground truth
                stage_06_scenario_decision.create_profile_scenario_answer_from_ground_truth(
                    path
                )

            # Create decision probability table
            stage_06_scenario_decision.create_decision_probability_table(path)

            print(display_progress.decision_probability_table_progess(path))
            print_end_stage()
        sys.exit()
    else:
        # Display Scenario answer saved path & Decision probability table
        print(display_progress.profile_scenario_answer_progess(path))
        print(display_progress.decision_probability_table_progess(path))


def run_generate_simulation_script(path: SystemPath):
    if not os.path.isfile(path.get_07_simulation_script_path()):
        stage_str = "Generate simulation script"
        proceed = ask_proceed(stage_str)
        if proceed:
            stage_07_script_generation.build_simulation_script(path)

            print_end_stage(True)
    else:
        print(display_progress.simulation_script_progess(path))
        print_end_stage(True)


def main(
    project_name: str,
):
    path = SystemPath(project_name)

    # NOTE: If result file(s) of a stage exist that means that stage is completed.
    # each run stage function (eg. run_setup_objective), check their result file(s) before run the stage.

    # Stage 00 Setup Project
    run_setup_project(path)

    # Stage 01 Setup Objective
    run_setup_topic_outline(path)

    # Stage 02 Build EABSS scope
    run_build_eabss(path)

    # Stage 03 Build EABSS diagrams
    run_build_eabss_usecase_diagramm(path)
    run_build_remaining_eabss_diagrams(path)

    # Stage 04 Define archetyp, scenario questions, scenarion answer choices
    run_design_profile_n_scenario(path)

    # Stage 05 Extract Profiles (& classify profile archetype)
    run_extract_profiles(path)

    # Stage 06 Create Decision probability table
    run_create_decision_probability_table(path)

    # Stage 07 Generate Simulation script
    run_generate_simulation_script(path)

    print()


if __name__ == "__main__":
    # NOTE: As Reminder - A List of Datasets

    # Sustanable Travel
    # Scope: "data/travel_scope_txt"
    # Profile: "data/travel_profile_txt"

    # Plastic Bag Charge
    # Scope: "data/diary_txt"
    # Profile: "data/diary_txt"

    parser = argparse.ArgumentParser("Main System")
    parser.add_argument("project_name", help="A project name", type=str)

    args = parser.parse_args()
    main(args.project_name)
