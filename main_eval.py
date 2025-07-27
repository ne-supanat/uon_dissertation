import os
import sys

import eval_02_build_eabss_evaluation
import stage_02_build_eabss_extra

import eval_05_profile_evaluation

import eval_06_scenario_decision_evaluation

from system_path import SystemPath
import display_progress

# TODO: add comments
# TODO: use BERTScore for summary result


def ask_continue() -> bool:
    approve = None
    while approve not in ["y", "n"]:
        approve = input(f"\nContinue? (y/n): ").lower()
    return approve == "y"


def run_evaluate_thematic_analysis(path: SystemPath):
    if os.path.isfile(path.get_02_thematic_analysis_path()):
        eval_02_build_eabss_evaluation.evaluate(path)
        # thematic_analysis_extra.analyse(source_paths)

        is_continue = ask_continue()
        if not is_continue:
            sys.exit()
    else:
        print(f"File not found: '{path.get_02_thematic_analysis_path()}'")
        sys.exit()


def run_evaluate_extract_profile(path: SystemPath):
    if os.path.isfile(path.get_05_profiles_path()):
        eval_05_profile_evaluation.evaluate(path)

        is_continue = ask_continue()
        if not is_continue:
            sys.exit()
    else:
        print(f"File not found: '{path.get_05_profiles_path()}'")
        sys.exit()


def run_evaluate_create_decision_probability_table(path: SystemPath):
    if os.path.isfile(path.get_06_profile_scenario_answers_path()):
        # Generate ground truth (For evaluation)
        if not os.path.isfile(path.get_eval_06_scenario_ground_truth_path()):
            eval_06_scenario_decision_evaluation.create_ground_truth(path)

        print(display_progress.ground_truth_progess(path))

        # Evaluate profile's answer
        eval_06_scenario_decision_evaluation.score_profile_anwsers(path)
    else:
        print(f"File not found: '{path.get_06_profile_scenario_answers_path()}'")
        sys.exit()


def main(project_name: str):
    path = SystemPath(project_name)
    if not os.path.isdir(project_name):
        print(f'No project name {project_name}. Please run "main.py" first.')
        sys.exit()

    # Evaluate thematic analysis
    run_evaluate_thematic_analysis(path)

    # Evaluate Profiles
    run_evaluate_extract_profile(path)

    # Create Decision probability table
    run_evaluate_create_decision_probability_table(path)

    print()


if __name__ == "__main__":
    # TODO: pick source & project from terminal (optional)
    project_name = "travel2"
    main(project_name)
