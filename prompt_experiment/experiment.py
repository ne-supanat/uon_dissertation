from typing import Literal
import json

import profile_generation
import profile_validation
import answer_generation
import answer_evaluation
import prompt_experiment.prompt as prompt


# TODO: lable / score type
def runExperimentOnce(
    prompt: prompt.Prompt,
    questionType: Literal["label", "score"],
    questions: list[dict] | list[str],
):
    # Extract profile
    profile = profile_generation.generateProfile(prompt)
    jsonProfile = json.loads(profile)

    # Evaluate profile
    # TODO: validityScore = evaluation_profile_validity.evaluateValidity(profile)

    # Complete tasks
    answers = answer_generation.answer(profile, questionType, questions)

    # Evaluate usability
    # use domain label/score depend on question type
    domainTagKey = "domain_label" if questionType == "label" else "domain_score"
    usabilityScore = answer_evaluation.evaluateAnswer(
        questionType,
        questions,
        jsonProfile[domainTagKey],
        answers,
    )

    return [
        profile,
        answers,
        0.5,  # validity_score
        usabilityScore,
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
