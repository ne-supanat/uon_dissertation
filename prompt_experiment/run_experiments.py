import os

import prompt_experiment.experiment as experiment
import prompt_experiment.prompt as p


def getContent(filePath):
    # Get interview content
    content = ""
    with open(filePath, "r") as f:
        content = f.read()

    return content


def main():
    topic = "Travelling destination preferences"
    labelDict = {
        "fav_warm": "people who like warm countries",
        "fav_cold": "people who like cold countries",
    }

    questionType = "label"
    questions = [
        {
            "question": "Pick 2 countries you want to go?",
            "choices": ["Thailand", "Spain", "Singapore", "England", "Norway"],
            "choice_values": [
                "fav_warm",
                "fav_warm",
                "fav_warm",
                "fav_cold",
                "fav_cold",
            ],
        },
        {
            "question": "Pick 2 activities you want to do?",
            "choices": [
                "Scuba Diving",
                "Swimming",
                "Nature Trails",
                "Skiing",
                "Ice Skating",
                "Sauna",
            ],
            "choice_values": [
                "fav_warm",
                "fav_warm",
                "fav_warm",
                "fav_cold",
                "fav_cold",
                "fav_cold",
            ],
        },
    ]

    pathSrc = f"data/DAICWOZ/txt"
    pathResult = f"results"

    interviewFilePaths = os.listdir(pathSrc)
    prompts: list[p.Prompt] = [
        p.PromptZeroShot,
        p.PromptFewShot,
    ]

    os.makedirs(pathResult, exist_ok=True)
    with open(f"{pathResult}/result.csv", "w") as f:
        f.write(f"File path;Prompt;Response;Validity score;Usability score\n")

    for interviewFilePath in interviewFilePaths[0:1]:
        print(interviewFilePath)
        interview = getContent(f"{pathSrc}/{interviewFilePath}")
        # TODO: drop some part of interview (drop 20-50%)

        for prompt in prompts:
            result = experiment.runExperimentOnce(
                prompt(
                    interview=interview,
                    topic=topic,
                    labelDict=labelDict,
                ),
                questionType,
                questions,
            )

            os.makedirs(pathResult, exist_ok=True)
            with open(f"{pathResult}/result.csv", "a+") as f:
                # result[0]: str    is Response
                # result[1]: float  is Validity score
                # result[2]: float  is Usability score

                f.write(
                    f"{interviewFilePath};{prompt.name()};{result[0].replace("\n", "")};{result[1]};{result[2]}\n"
                )


if __name__ == "__main__":
    main()
