import os
import sys

import eval_02_build_eabss_evaluation
import stage_02_build_eabss_extra

import eval_05_profile_evaluation

import eval_06_scenario_decision_evaluation

# TODO: add comments


def get_transcript_file_paths(source_path):
    # return ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    return [
        f"{source_path}/{filename}" for filename in sorted(os.listdir(source_path))[0:5]
    ]


def print_end_stage(is_last_stage: bool = False):
    if not is_last_stage:
        print("\nRun 'main.py' to continue to the next stage.\n")
    else:
        print("-" * 50 + "\nAll model development stages completed\n" + "=" * 50)
        print("\nRun 'main_post.py' to analyse the model output.\n")


def main(source_folder: str, results_folder: str):
    # source_paths = get_transcript_file_paths(source_folder)
    results_path = results_folder
    if not os.path.isdir(results_path):
        print(f'No project name {results_path}. Please run "main.py" first.')
        sys.exit()

    ## Evaluate thematic analysis
    ta_codes_txt_path = os.path.join(results_path, "02_thematic_analysis_codes.txt")
    if os.path.isfile(ta_codes_txt_path):
        eval_02_build_eabss_evaluation.evaluate(ta_codes_txt_path)
        # thematic_analysis_extra.analyse(source_paths)

    ## Evaluate Profiles
    profiles_path = os.path.join(results_path, "05_profiles.txt")
    if not os.path.isfile(profiles_path):
        eval_05_profile_evaluation.evaluate(profiles_path)

    ## Create Decision probability table
    scenario_questions_path = os.path.join(results_path, "04_scenario_questions.txt")
    scenario_choices_path = os.path.join(results_path, "04_scenario_choices.txt")

    profile_scenario_answers_path = os.path.join(
        results_path, "06_profile_scenario_answers.csv"
    )
    decision_probability_path = os.path.join(
        results_path, "06_scenario_probability.csv"
    )

    # if not os.path.isfile(decision_probability_path):
    #     # Generate ground truth
    #     scenario_ground_truth_path = os.path.join(
    #         results_path, "scenario_ground_truth.txt"
    #     )
    #     scenario_scores_path = os.path.join(results_path, "scenario_scores.csv")
    #     eval_06_scenario_decision_evaluation.generate_ground_truth(
    #         scenario_questions_path,
    #         scenario_ground_truth_path,
    #     )

    #     # Evaluate profile's answer
    #     eval_06_scenario_decision_evaluation.score_profile_anwsers(
    #         scenario_ground_truth_path,
    #         profile_scenario_answers_path,
    #         scenario_scores_path,
    #     )

    print()


if __name__ == "__main__":
    source_folder = "data/diary_txt"
    results_folder = "results_5"
    # TODO: pick source & project from terminal (optional)
    main(source_folder, results_folder)
