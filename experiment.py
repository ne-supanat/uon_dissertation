import extract_profile
import evaluation_profile_validity
import evaluation_profile_usability
import prompt


def runExperimentOnce(prompt):
    profile = extract_profile.extractProfile(prompt)
    # print(profile)

    # TODO: evaluation
    # valid = evaluation_profile_validity.evaluateValidity(profile)
    # usability = evaluation_profile_usability.evaluateUsability(profile)
    # TODO: write record


if __name__ == "__main__":
    topic = "Travelling destination preferences"
    labelDict = {
        "fav_warm": "people who like warm countries",
        "fav_cold": "people who like cold countries",
    }

    # evaluationQuestion = {}
    # evaluationAnswer = {}

    interview = ""
    with open("data/DAICWOZ/txt/HIGH_321_TRANSCRIPT.txt", "r") as f:
        interview = f.read()

    runExperimentOnce(
        prompt.PromptZeroShot(interview=interview, topic=topic, labelDict=labelDict),
    )
