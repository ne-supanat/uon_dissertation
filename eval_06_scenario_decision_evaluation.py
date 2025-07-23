import os
import json
import numpy as np

import paths


def score_profile_anwsers(
    archetype_path,
    scenario_ground_truth_path,
    scenario_answers_path,
    scenario_scores_path,
):
    scores = {}

    with open(scenario_ground_truth_path, "r") as f:
        ground_truth = json.loads(f.read())

    with open(archetype_path, "r") as f:
        content = f.read()
        archetypes = content.strip().splitlines()

    with open(scenario_answers_path, "r") as f:
        content = f.read()
        rows = content.strip().splitlines()

        # CSV format
        # --------------------------
        # file;archetype;answer of question 1;answer of question 2;...

        for row in rows:
            line_split = row.strip().split(";")
            file = line_split[0]
            archetype = line_split[1]
            archetype_index = archetypes.index(archetype)
            answers = line_split[2:]

            match_answer = 0
            for i, answer in enumerate(answers):
                # Check if profile's answer is in answers of profile's archetype
                if answer in ground_truth[i][archetype_index]:
                    match_answer += 1

            scores[file] = match_answer / len(answers)

    print("-" * 50)
    print("Profile's Scenario Answers Evaluation")
    print("-" * 50)
    for document, score in scores.items():
        print(f"{document:<{len(file)+2}}: {score:.2f}")

    print("-" * 50)
    print(
        f"Profile's Scenario Answers Evaluation - Mean score: {np.mean(list(scores.values())):.2f}"
    )
    print("-" * 50)
    print()

    with open(scenario_scores_path, "w") as f:
        f.write(
            "\n".join(
                [f"{document};{score:<.2f}" for document, score in scores.items()]
            )
        )

    print(f"Result saved to: '{scenario_scores_path}'")


if __name__ == "__main__":
    results_path = "results_4"

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

    score_profile_anwsers(
        archetype_path,
        scenario_ground_truth_path,
        profile_scenario_answers_path,
        scenario_scores_path,
    )
