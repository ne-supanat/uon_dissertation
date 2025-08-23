import argparse
import os
import sys

import stage_00_project_setup
import stage_01_outline_setup
import stage_02_build_scope
import stage_03_generate_diagram
import stage_04_archetype_scenario_setup
import stage_05_profile_extraction
import stage_06_scenario_decision
import stage_07_script_generation

import display_result
from system_path import SystemPath
import utils

# TODO: add comments


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
        print("\nRun 'main.py' to review the result.")


def run_setup_project(path: SystemPath):
    if not os.path.isdir(path.project_name):
        # Start new project
        print("\nNo existing project detected.")
        print("Starting new project...")

        stage_00_project_setup.run_setup_project(path)
    else:
        display_result.display_header()


def run_setup_topic_outline(path: SystemPath):
    if not os.path.isfile(path.get_01_topic_path()) or not os.path.isfile(
        path.get_01_outline_path()
    ):
        # Setup topic and outline of the model
        stage_01_outline_setup.setup_topic(path)
        print()
        stage_01_outline_setup.setup_outline(path)

        # Display topic & outline of the model
        print(display_result.topic_outline_result(path))

        print_end_stage()
        sys.exit()
    else:
        # Display topic & outline of the model
        print(display_result.topic_outline_result(path))


def run_build_model_scope(path: SystemPath):
    if not os.path.isfile(path.get_02_model_scope_path()):
        stage_str = "Building The Model Scope"
        proceed = ask_proceed(stage_str)

        if proceed:
            # Thematic analysis
            scope_document_paths = utils.get_transcript_file_paths(
                path.get_scope_data_directory_path()
            )
            stage_02_build_scope.run_thematic_analysis(path, scope_document_paths)
            print()

            # Finalise model scope
            stage_02_build_scope.run_model_scope_finalisation(path)

            # Display model scope result
            print(display_result.model_scope_result(path))
            print_end_stage()

        sys.exit()
    else:
        # Display model scope result
        print(display_result.model_scope_result(path))


def run_build_model_usecase_diagramm(path: SystemPath):
    if not os.path.isfile(path.get_03_model_usecase_diagram_path()):
        stage_str = "Creating model diagrams - use case diagram"
        proceed = ask_proceed(stage_str)
        if proceed:
            # Create usecase diagrams
            stage_03_generate_diagram.build_usecase_diagrams(path)

            print_end_stage()
        sys.exit()
    else:
        # Display usecase diagrams result
        print(display_result.diagram_header())
        print(display_result.model_usecase_diagrams_result(path))


def should_build_remaining_model_diagrams(path: SystemPath):
    # Check if any of remaining diagram result files does not exist.
    return (
        not os.path.isfile(path.get_03_model_activity_diagram_path())
        or not os.path.isfile(path.get_03_model_state_diagram_path())
        or not os.path.isfile(path.get_03_model_interaction_diagram_path())
        or not os.path.isfile(path.get_03_model_class_diagram_path())
    )


def run_build_remaining_model_diagrams(path: SystemPath):
    if should_build_remaining_model_diagrams(path):
        stage_str = "Creating model diagrams - remaining diagrams"
        proceed = ask_proceed(stage_str)
        if proceed:
            # Generate remaining diagrams
            stage_03_generate_diagram.build_remaining_diagrams(path)

            print_end_stage()
        sys.exit()
    else:
        # Display remaining diagrams result
        print(display_result.model_diagrams_result(path))


def should_design_profile_n_scenario(path: SystemPath):
    # Check if any of result files of design and profile step does not exist.
    return (
        not os.path.isfile(path.get_04_archetypes_path())
        or not os.path.isfile(path.get_04_attributes_path())
        or not os.path.isfile(path.get_04_scenario_path())
    )


def run_design_profile_n_scenario(path: SystemPath):
    if should_design_profile_n_scenario(path):
        stage_str = "Design Profile and Scenario"
        proceed = ask_proceed(stage_str)
        if proceed:
            # Design profile & scenarion
            stage_04_archetype_scenario_setup.design_profile_n_scenario(path)

            display_result.display_stage04(path)
            print_end_stage()
        sys.exit()
    else:
        # Display Archetype, Attributes, Scenario saved locations
        display_result.display_stage04(path)


def run_extract_profiles(path: SystemPath):
    if not os.path.isfile(path.get_05_profiles_path()):
        stage_str = "Extract profiles"
        proceed = ask_proceed(stage_str)
        if proceed:
            # Extract profile
            profile_document_paths = utils.get_transcript_file_paths(
                path.get_profile_data_directory_path()
            )
            stage_05_profile_extraction.extract_profile(path, profile_document_paths)

            print_end_stage()
        sys.exit()
    else:
        # Display Profiles saved location
        print(display_result.profile_result(path))


def run_create_decision_probability_table(path: SystemPath):
    if not os.path.isfile(path.get_06_decision_probability_path()):
        stage_str = "Decision probability table"
        proceed = ask_proceed(stage_str)
        if proceed:
            # Ask user to use profile-based or archetype-based
            # to create scenario answers
            with open(path.get_04_archetypes_path(), "r") as f:
                archetypes = f.read().strip().splitlines()
            archetypes_size = len(archetypes)

            with open(path.get_04_scenario_path(), "r") as f:
                questions = f.read().strip().splitlines()

            with open(path.get_05_profiles_path(), "r") as f:
                content = f.read()
            profiles = [profile for profile in content.strip().split("\n\n")]
            profiles_size = len(profiles)

            print()
            print(
                f"Select the method to answer the scenario question{"s" if len(questions) > 1 else ""}"
            )
            print(
                f"1. Use profile-based approach ({profiles_size} profile{"s" if profiles_size>1 else ""})"
            )
            print(
                f"2. Use archetype-based approach ({archetypes_size} archetype{"s" if archetypes_size>1 else ""})"
            )

            method = None
            while method not in ["1", "2"]:
                method = input(f"\nEnter the method number (1 or 2): ").lower()

            # Answer scenario questions
            if method == "1":
                # Based on extracted profile(s)
                stage_06_scenario_decision.create_decision_profile_answers(path)
                print(display_result.decision_profile_result(path))

                # Create decision probability table
                stage_06_scenario_decision.create_decision_profile_table(path)
            elif method == "2":
                # Based on archetypes
                stage_06_scenario_decision.create_decision_archetype(path)
                print(display_result.decision_archetype_result(path))

                # Create decision probability table
                stage_06_scenario_decision.create_decision_archetype_table(path)

            print(display_result.decision_probability_table_result(path))
            print_end_stage()
        sys.exit()
    else:
        # Display Decision probability table saved path
        print(display_result.decision_probability_table_result(path))


def run_generate_simulation_script(path: SystemPath):
    if not os.path.isfile(path.get_07_simulation_script_path()):
        stage_str = "Generate simulation script"
        proceed = ask_proceed(stage_str)
        if proceed:
            stage_07_script_generation.build_simulation_script(path)

            print_end_stage(True)
    else:
        print(display_result.simulation_script_result(path))
        print_end_stage(True)


def main(
    project_name: str,
):
    path = SystemPath(project_name)

    # NOTE: If result file(s) of a stage exist that means that stage is completed.
    # each run stage function (eg. run_setup_objective), check their result file(s) before run the stage.

    # Stage 00 Setup Project
    run_setup_project(path)

    # Stage 01 Setup model outline
    run_setup_topic_outline(path)

    # Stage 02 Build model scope
    run_build_model_scope(path)

    # Stage 03 Build model diagrams
    run_build_model_usecase_diagramm(path)
    run_build_remaining_model_diagrams(path)

    # Stage 04 Design profile, scenario
    run_design_profile_n_scenario(path)

    # Stage 05 Extract Profiles (& classify profile archetype)
    run_extract_profiles(path)

    # Stage 06 Create Decision probability table
    run_create_decision_probability_table(path)

    # Stage 07 Generate Simulation script
    run_generate_simulation_script(path)

    print()


if __name__ == "__main__":
    # NOTE: (As Reminder) - A List of Datasets
    # Scope: data/travel_scope_txt
    # Profile: data/travel_profile_txt

    parser = argparse.ArgumentParser("Main System")
    parser.add_argument("project_name", help="A project name", type=str)

    args = parser.parse_args()
    main(args.project_name)
