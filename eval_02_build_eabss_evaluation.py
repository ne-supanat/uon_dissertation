import os
import json
import numpy as np


def evaluate(thematic_analysis_codes_txt_path: str, thematic_analysis_scores_path: str):
    ## Check quotes do exist in file
    not_found_dict = {}
    total_quote_dict = {}
    scores = {}

    # Read thematic analysis result
    with open(thematic_analysis_codes_txt_path, "r") as f:
        text = f.read()

    # Check each document (transcript)
    documents = text.strip().split("\n\n")
    for document_raw in documents:
        document: dict = json.loads(document_raw)

        file = document["file"]
        not_found_dict[file] = []
        total_quote_dict[file] = 0

        with open(file, "r") as f:
            lines = f.read().splitlines()  # transcript lines

        # Check each component (actors, archetypes, physical_components, social_aspect, psychological_aspect, misc, key_activities)
        for key in document.keys():
            if key == "file":
                continue
            for item in document[key]:
                for quote in item["quotes"]:
                    found = False
                    for line in lines:
                        # Check if can find quote speak by Participant
                        if quote.lower() in line.lower() and line.startswith(
                            "Participant: "
                        ):
                            found = True

                    if not found:
                        not_found_dict[file].append(quote)

            total_quote_dict[file] += len(document[key])

        scores[file] = 1 - (len(not_found_dict[file]) / (total_quote_dict[file]))

    print("-" * 50)
    print("Thematic Analysis Evaluation")
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

    print(
        f"Thematic Analysis Evaluation - Mean match score: {np.mean(list(scores.values())):.2f}"
    )
    print("-" * 50)
    print()

    with open(thematic_analysis_scores_path, "w") as f:
        f.write(
            "\n".join(
                [f"{document};{score:<.2f}" for document, score in scores.items()]
            )
        )
    print(f"Result saved to: '{thematic_analysis_scores_path}'")


if __name__ == "__main__":
    results_path = "results_4"
    ta_codes_txt_path = os.path.join(results_path, "02_thematic_analysis_codes.txt")
    ta_codes_txt_path = os.path.join(results_path, "02_thematic_analysis_codes.txt")

    evaluate(ta_codes_txt_path, "")
