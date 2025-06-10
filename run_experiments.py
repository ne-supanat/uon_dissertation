import os

import experiment
import prompt as p


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

    # evaluationQuestion = {}
    # evaluationAnswer = {}

    pathSrc = f"data/DAICWOZ/txt/"
    pathResult = f"results/"

    interviewFilePaths = os.listdir(pathSrc)
    prompts = [p.PromptZeroShot]

    for interviewFilePath in interviewFilePaths[0:1]:
        print(interviewFilePath)
        interview = getContent(pathSrc + interviewFilePath)
        for prompt in prompts:
            result = experiment.runExperimentOnce(
                prompt(interview=interview, topic=topic, labelDict=labelDict),
            )

            # TODO: record: interview, prompt, response, score
            # os.makedirs(pathResult, exist_ok=True)


if __name__ == "__main__":
    main()
