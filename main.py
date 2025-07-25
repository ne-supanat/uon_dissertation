import os
import sys

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


def get_transcript_file_paths(source_path):
    return [
        f"{source_path}/{filename}" for filename in sorted(os.listdir(source_path))[0:1]
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


def run_setup_objective(path: SystemPath):
    if not os.path.isfile(path.get_01_objective_path()):
        # New project
        print("\nNo existing project detected.")
        print("Starting new project...")
        stage_01_objective_setup.setup_objective(path)

        print(display_progress.setup_objective_progress(path))

        print_end_stage()
        sys.exit()
    else:
        # Display objective result
        display_progress.display_header()
        print(display_progress.setup_objective_progress(path))


def run_build_eabss(path: SystemPath, document_paths: list[str]):
    if not os.path.isfile(path.get_02_eabss_scope_path()):
        stage_str = "Build EABSS components"
        proceed = ask_proceed(stage_str)

        if proceed:
            # Thematic analysis
            stage_02_build_eabss.run_thematic_analysis(path, document_paths)
            print()

            # Finalise EABSS components
            stage_02_build_eabss.run_eabss_scope_finalisation(path)

            # Display EABSS components result
            print(display_progress.eabss_components_progress(path))
            print_end_stage()

        sys.exit()
    else:
        # Display EABSS components result
        print(display_progress.eabss_components_progress(path))


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


def run_extract_profiles(path: SystemPath, document_paths: list[str]):
    if not os.path.isfile(path.get_05_profiles_path()):
        stage_str = "Extract profiles"
        proceed = ask_proceed(stage_str)
        if proceed:
            # Extract profile
            stage_05_profile_extraction.extract_profile(path, document_paths)

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
            # Answer scenario-questions
            if not os.path.isfile(path.get_06_profile_scenario_answers_path()):
                stage_06_scenario_decision.create_profile_scenario_answers(path)

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


def main(source_folder: str, project_name: str):
    document_paths = get_transcript_file_paths(source_folder)
    os.makedirs(project_name, exist_ok=True)

    path = SystemPath(project_name)

    # NOTE: If result file(s) of a stage exist that means that stage is completed.
    # each run stage function (eg. run_setup_objective), check their result file(s) before run the stage.

    # Stage 01 Setup Objective
    run_setup_objective(path)

    # Build EABSS scope
    run_build_eabss(path, document_paths)

    # Build EABSS diagrams
    run_build_eabss_usecase_diagramm(path)
    run_build_remaining_eabss_diagrams(path)

    # Define archetyp, scenario questions, scenarion answer choices
    run_design_profile_n_scenario(path)

    # Extract Profiles (& classify profile archetype)
    run_extract_profiles(path, document_paths)

    # Create Decision probability table
    run_create_decision_probability_table(path)

    ## Generate Simulation script
    run_generate_simulation_script(path)

    print()


if __name__ == "__main__":
    # source_folder = "data/diary_txt"
    source_folder = "data/mvp"
    project_name = "test"
    # TODO: pick source & project from terminal (optional)
    main(source_folder, project_name)
