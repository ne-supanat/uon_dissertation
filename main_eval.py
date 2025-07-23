import os
import sys

import eval_02_build_eabss_evaluation
import stage_02_build_eabss_extra

import eval_05_profile_evaluation

import eval_06_scenario_decision_evaluation

import paths

# TODO: add comments


def ask_proceed() -> bool:
    approve = None
    while approve not in ["y", "n"]:
        approve = input(f"\nContinue? (y/n): ").lower()
    return approve == "y"


def main(results_folder: str):
    results_path = results_folder
    if not os.path.isdir(results_path):
        print(f'No project name {results_path}. Please run "main.py" first.')
        sys.exit()

    ## Evaluate thematic analysis
    ta_codes_txt_path = os.path.join(results_path, paths.thematic_codes_file_path)
    thematic_analysis_score_path = os.path.join(
        results_path, paths.thematic_analysis_score_file_path
    )
    if os.path.isfile(ta_codes_txt_path):
        eval_02_build_eabss_evaluation.evaluate(
            ta_codes_txt_path, thematic_analysis_score_path
        )
        # thematic_analysis_extra.analyse(source_paths)

        proceed = ask_proceed()
        if not proceed:
            sys.exit()

    ## Evaluate Profiles
    profiles_path = os.path.join(results_path, paths.profile_file_path)
    profile_quotes_score_path = os.path.join(
        results_path, paths.profile_quotes_score_file_path
    )
    if os.path.isfile(profiles_path):
        eval_05_profile_evaluation.evaluate(profiles_path, profile_quotes_score_path)

        proceed = ask_proceed()
        if not proceed:
            sys.exit()

    ## Create Decision probability table
    archetype_path = os.path.join(results_path, paths.archetype_file_path)
    scenario_ground_truth_path = os.path.join(
        results_path, paths.scenario_ground_truth_file_path
    )
    profile_scenario_answers_path = os.path.join(
        results_path, paths.profile_scenario_answers_file_path
    )

    scenario_scores_path = os.path.join(
        results_path, paths.scenario_answer_score_file_path
    )

    if os.path.isfile(profile_scenario_answers_path):
        # Evaluate profile's answer
        eval_06_scenario_decision_evaluation.score_profile_anwsers(
            archetype_path,
            scenario_ground_truth_path,
            profile_scenario_answers_path,
            scenario_scores_path,
        )

    print()


if __name__ == "__main__":
    results_folder = "results_4"
    # TODO: pick source & project from terminal (optional)
    main(results_folder)
