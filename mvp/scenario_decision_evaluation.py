import json

import llm
from response_models import TransportationMode, Archetype


def generate_ground_truth(questions: list[str]):
    prompt = f"""
Archetypes are {", ".join([type.value for type in Archetype])}
Choices are {", ".join([type.value for type in TransportationMode])}

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
    response = llm.generate_content(prompt, list[list[list[TransportationMode]]])
    with open(f"mvp/results/scenario_ground_truth.txt", "w") as f:
        f.write(response.text)


def score_anwser():
    with open(f"mvp/results/scenario_ground_truth.txt", "r") as fr:
        ground_truth: list[list[list[TransportationMode]]] = json.loads(fr.read())

    with open(f"mvp/results/scenario_answer_record.csv", "r") as fr:
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

            with open(f"mvp/results/scenario_question_score.csv", "a+") as fw:
                fw.write(f"{file};{score / len(answers)}\n")

            line = fr.readline()


if __name__ == "__main__":
    # with open(f"mvp/results/scenario_questions.txt", "r") as f:
    #     questions = json.loads(f.read())
    #     generate_ground_truth(questions)

    score_anwser()
