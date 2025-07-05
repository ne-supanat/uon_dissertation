import pandas as pd
import json

from response_models import Archetype, TransportationMode


def generate(scenario_questions_path, scenario_answers_path, scenario_probability_path):
    with open(scenario_questions_path, "r") as f:
        questions = json.loads(f.read())

    df = pd.read_csv(scenario_answers_path, sep=";", header=None)
    df.columns = ["file", "type"] + [f"q{i+1}" for i in range(len(questions))]

    with open(scenario_probability_path, "w") as f:
        for type in Archetype:
            archetype_df = df[df["type"] == type.value]
            archetype_size = archetype_df.shape[0]

            for i in range(len(questions)):
                for mode in TransportationMode:
                    answer_df = archetype_df[archetype_df[f"q{i+1}"] == mode.value]

                    if archetype_size:
                        prob = answer_df.shape[0] / archetype_size
                    else:
                        prob = 0

                    print(f"{type.value};{questions[i]};{mode.value};{prob}")
                    f.write(f"{type.value};{questions[i]};{mode.value};{prob}\n")


if __name__ == "__main__":
    scenario_questions_path = "abm_analysis/results/scenario_questions.txt"
    scenario_answers_path = "abm_analysis/results/scenario_answers.csv"
    scenario_probability_path = "abm_analysis/results/scenario_probability.csv"

    generate(scenario_questions_path, scenario_answers_path, scenario_probability_path)
