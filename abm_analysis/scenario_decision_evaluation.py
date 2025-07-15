import json

import llm
from models.archetypes import Archetype
from models.scenario_choices import ScenarioChoice


def generate_ground_truth(scenario_questions_path, scenario_ground_truth_path):
    with open(scenario_questions_path, "r") as f:
        questions = json.loads(f.read())

    prompt = f"""
Archetypes are {", ".join([type.value for type in Archetype])}
Choices are {", ".join([type.value for type in ScenarioChoice])}

What archetype each choice belong (choice can be in one, both or none of the archetypes)

Give answers for the following questions:
{questions}

in this format

{"{"}[
[[choice1,choice2],[choice3,choice4]],
[[choice1,choice2],[choice3,choice4]],
]{"}"}

which is

{"{"}[
[[Choices belong to Archetype 1 of Question 1], [Choices belong to Archetype 2 of Question 1]],
[[Choices belong to Archetype 1 of Question 2], [Choices belong to Archetype 2 of Question 2]],
]{"}"}
"""
    response = llm.generate_content(prompt, list[list[list[ScenarioChoice]]])
    with open(scenario_ground_truth_path, "w") as f:
        f.write(response.text)


def score_profile_anwsers(
    scenario_ground_truth_path, scenario_answers_path, scenario_scores_path
):
    with open(scenario_ground_truth_path, "r") as fr:
        ground_truth: list[list[list[ScenarioChoice]]] = json.loads(fr.read())

    with open(scenario_answers_path, "r") as fr:
        line = fr.readline()
        while line:
            line_split = line.strip().split(";")
            file = line_split[0]
            archetype = line_split[1]
            archetype_index = [type.value for type in Archetype].index(archetype)
            answers = line_split[2:]

            score = 0
            for i, answer in enumerate(answers):
                if answer in ground_truth[i][archetype_index]:
                    score += 1

            with open(scenario_scores_path, "a+") as fw:
                fw.write(f"{file};{score / len(answers)}\n")

            line = fr.readline()


if __name__ == "__main__":
    scenario_questions_path = "abm_analysis/results/scenario_questions.txt"
    scenario_ground_truth_path = "abm_analysis/results/scenario_ground_truth.txt"

    scenario_answers_path = "abm_analysis/results/scenario_answers.csv"
    scenario_scores_path = "abm_analysis/results/scenario_scores.csv"

    generate_ground_truth(
        scenario_questions_path,
        scenario_ground_truth_path,
    )

    score_profile_anwsers(
        scenario_ground_truth_path, scenario_answers_path, scenario_scores_path
    )
