import os
import json
import numpy as np

from models.response_models import Profile


def evaluate(profiles_path: str):
    ## Check quotes do exist in file
    not_found_dict = {}
    total_quote_dict = {}
    scores = []

    # Read profile analysis result
    with open(profiles_path, "r") as f:
        text = f.read()

    # Check each document (transcript)
    profiles = text.strip().split("\n\n")
    for profile_raw in profiles:
        profile: dict = json.loads(profile_raw)

        file = profile["file"]
        not_found_dict[file] = []
        total_quote_dict[file] = 0

        with open(file, "r") as f:
            lines = f.read().splitlines()  # transcript lines

        for quote in profile["quotes"]:
            found = False
            for line in lines:
                if quote.lower() in line.lower() and line.startswith("Participant: "):
                    found = True

            if not found:
                not_found_dict[file].append(quote)

        total_quote_dict[file] += len(profile["quotes"])
        scores.append(1 - (len(not_found_dict[file]) / (total_quote_dict[file])))

    print("-" * 50)
    print("Profile's Quotes Evaluation")
    print("-" * 50)
    for document in not_found_dict.keys():
        print()
        for name, value in zip(
            [
                "File",
                "Match Score",
                "Total quotes",
                "Missing quotes",
            ],
            [
                document,
                f"{1 - (len(not_found_dict[document]) / (total_quote_dict[document])):.2f}",
                total_quote_dict[file],
                len(not_found_dict[document]),
            ],
        ):
            print(f"{name:<15}: {value:<10}")

        if len(not_found_dict[document]):
            print()
            print("Missing Quote:")
            for quote in not_found_dict[document]:
                print(f"- {quote}")
        print()
        print("-" * 50)

    print(f"Profile's Quotes  Evaluation - Mean match score: {np.mean(scores):.2f}")
    print("-" * 50)
    print()


if __name__ == "__main__":
    results_path = "results_4"
    profiles_path = os.path.join(results_path, "05_profiles.txt")
    evaluate(profiles_path)
