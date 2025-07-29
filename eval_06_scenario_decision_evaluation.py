import json
import numpy as np

import llm
from models.archetypes import Archetype
from models.scenario_choices import ScenarioChoice

from system_path import SystemPath


def score_profile_anwsers(path: SystemPath):
    scores = {}

    with open(path.get_06_scenario_ground_truth_path(), "r") as f:
        ground_truth = json.loads(f.read())

    with open(path.get_04_archetypes_path(), "r") as f:
        content = f.read()
        archetypes = content.strip().splitlines()

    with open(path.get_06_profile_scenario_answers_path(), "r") as f:
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
    print()

    for document, score in scores.items():
        print(f"{document:<{len(file)+2}}: {score:.2f}")

    print()
    print("-" * 50)
    print(
        f"Profile's Scenario Answers Evaluation - Mean score: {np.mean(list(scores.values())):.2f}"
    )
    print("-" * 50)
    print()

    with open(path.get_eval_06_profile_scenario_answer_score_path(), "w") as f:
        f.write(
            "\n".join(
                [f"{document};{score:<.2f}" for document, score in scores.items()]
            )
        )

    print(f"Result saved to: '{path.get_eval_06_profile_scenario_answer_score_path()}'")


if __name__ == "__main__":
    path = SystemPath("travel2")
    score_profile_anwsers(path)
