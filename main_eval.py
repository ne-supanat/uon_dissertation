import argparse
import os
import sys

import eval_02_build_eabss_evaluation
import stage_02_build_eabss_extra

import eval_05_profile_evaluation

import eval_06_scenario_decision_evaluation

from system_path import SystemPath
import display_progress

from bert_score import BERTScorer

# TODO: add comments

# TODO: result reflect form (for better structure review)


def ask_continue() -> bool:
    approve = None
    while approve not in ["y", "n"]:
        approve = input(f"\nContinue? (y/n): ").lower()
    return approve == "y"


def run_evaluate_thematic_analysis(path: SystemPath, show_all: bool):
    if os.path.isfile(path.get_02_thematic_analysis_path()):
        eval_02_build_eabss_evaluation.evaluate(path)
        # thematic_analysis_extra.analyse(source_paths)
    else:
        print(f"File not found: '{path.get_02_thematic_analysis_path()}'")


def run_evaluate_extract_profile(path: SystemPath, show_all: bool):
    if os.path.isfile(path.get_05_profiles_path()):
        eval_05_profile_evaluation.evaluate(path)
    else:
        print(f"File not found: '{path.get_05_profiles_path()}'")


def run_evaluate_create_decision_probability_table(path: SystemPath):
    if os.path.isfile(path.get_06_profile_scenario_answers_path()):
        eval_06_scenario_decision_evaluation.score_profile_anwsers(path)
    else:
        print(f"File not found: '{path.get_06_profile_scenario_answers_path()}'")


def main(project_name: str, show_all: bool):
    path = SystemPath(project_name)
    if not os.path.isdir(project_name):
        print(f'No project name {project_name}. Please run "main.py" first.')
        sys.exit()

    # # Evaluate thematic analysis
    # run_evaluate_thematic_analysis(path, show_all)
    # print()

    # # Evaluate Profiles
    # run_evaluate_extract_profile(path, show_all)
    # print()

    # Create Decision probability table
    run_evaluate_create_decision_probability_table(path)

    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Main Evaluation")
    parser.add_argument("project_name", help="A project name", type=str)
    parser.add_argument(
        "--all", action="store_true", help="Show all evaluation stage without asking"
    )

    args = parser.parse_args()
    main(args.project_name, args.all)
