import os
import csv
from models.archetypes import Archetype
from models.scenario_choices import ScenarioChoice


def generate(
    scenario_questions_path,
    profile_scenario_answers_path,
    decision_probability_path,
):
    # Fetch scenario questions
    with open(scenario_questions_path, "r") as f:
        questions = f.read().strip().split("\n")

    # Initialize answer and archetype counters
    answer_dict = {
        question: {
            archetype.value: {choice.value: 0 for choice in ScenarioChoice}
            for archetype in Archetype
        }
        for question in questions
    }
    archetype_counts = {archetype.value: 0 for archetype in Archetype}

    # Read scenario answers
    with open(profile_scenario_answers_path, newline="") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            if not row or len(row) < 2 + len(questions):
                continue  # skip malformed rows
            archetype = row[1]
            archetype_counts[archetype] += 1
            for i, question in enumerate(questions):
                choice = row[2 + i]  # skip first 2 columns of filename and archetype
                answer_dict[question][archetype][choice] += 1

    # Write probabilities to output file
    with open(decision_probability_path, "w") as f:
        for question in questions:
            for archetype in Archetype:
                count = archetype_counts[archetype.value]
                probs = [
                    (
                        answer_dict[question][archetype.value][choice.value] / count
                        if count > 0
                        else 0
                    )
                    for choice in ScenarioChoice
                ]

                line = (
                    f"{question};{archetype.value};"
                    + ";".join(f"{p:.2f}" for p in probs)
                    + "\n"
                )
                f.write(line)
    print(f"\nDecision probability table saved to: '{decision_probability_path}'\n")


if __name__ == "__main__":
    results_path = "results_2"

    scenario_questions_path = os.path.join(results_path, "scenario_questions.txt")
    profile_scenario_answers_path = os.path.join(
        results_path, "profile_scenario_answers.csv"
    )
    decision_probability_path = os.path.join(results_path, "scenario_probability.csv")

    generate(
        scenario_questions_path,
        profile_scenario_answers_path,
        decision_probability_path,
    )
