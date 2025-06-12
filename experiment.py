from typing import Literal

import extract_profile
import evaluation_profile_validity
import evaluation_profile_usability
import prompt


# TODO: lable / score type
def runExperimentOnce(
    prompt: prompt.Prompt,
    questionType: Literal["label", "score"],
    questions: list[dict | str],
):
    profile = extract_profile.generateProfile(prompt)

    # TODO: add get answer first before evaluate

    # TODO: evaluation
    # TODO: valid = evaluation_profile_validity.evaluateValidity(profile)

    usabilityScore = evaluation_profile_usability.evaluateUsability(
        profile, questionType, questions
    )

    return [
        profile,  # profile
        0.5,  # validity_score
        usabilityScore,  # usability_score
    ]


if __name__ == "__main__":
    interview = ""
    with open("data/DAICWOZ/txt/HIGH_321_TRANSCRIPT.txt", "r") as f:
        interview = f.read()

    topic = "Travelling destination preferences"
    labelDict = {
        "fav_warm": "people who like warm countries",
        "fav_cold": "people who like cold countries",
    }

    # Label mode
    questionType = "label"
    questions = [
        {
            "type": "individual",
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
    ]

    runExperimentOnce(
        # prompt.PromptZeroShot(interview=interview, topic=topic, labelDict=labelDict),
        prompt.PromptFewShot(interview=interview, topic=topic, labelDict=labelDict),
        questionType,
        questions,
    )

    # # Score mode
    # questionType = "score"
    # questions = [
    #     "You love warm countries",
    #     "You love summer season",
    #     "You like rain and snow",
    # ]

    # runExperimentOnce(
    #     # prompt.PromptZeroShot(interview=interview, topic=topic, labelDict=labelDict),
    #     prompt.PromptFewShot(interview=interview, topic=topic, labelDict=labelDict),
    #     questionType,
    #     questions,
    # )
