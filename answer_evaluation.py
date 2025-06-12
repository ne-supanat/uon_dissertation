from typing import Literal


def evaluateAnswer(
    questionType: Literal["label", "score"],
    questions: list[dict] | list[str],
    domainTag: str,
    answers: list[str] | list[float],
) -> float:

    if questionType == "label":
        return evaluateLabelQuestions(questions, domainTag, answers)
    if questionType == "score":
        domainTag = float(domainTag)
        return evaluateScoreQuestions(questions, domainTag, answers)


def evaluateLabelQuestions(
    questions: list[dict],
    domainLabel: str,
    answers: list[str],
) -> float:
    scores = []
    for index, question in enumerate(questions):
        choices: list[str] = question["choices"]
        choiceValues: list[str] = question["choice_values"]

        answerItems = answers[index]

        if answerItems:
            countCorrectItems = 0
            for item in answerItems:
                # TODO: size of answer item more that asked

                if item not in choices:
                    raise Exception("Selected item is not in the choices")

                # correct item is item that hidden value matches the domain label
                if choiceValues[choices.index(item)] == domainLabel:
                    countCorrectItems += 1
            # precision: percentage of correct items from selected items
            precision = countCorrectItems / len(answerItems)
        else:
            precision = 0.0
        scores.append(precision)

    meanScore = sum(scores) / len(questions)

    print(scores)
    print(f"Mean Score: {meanScore}")
    return meanScore


def evaluateScoreQuestions(
    domainScore: float,
    answers: list[float],
) -> float:
    error = abs(sum(answers) - domainScore)

    print(answers)
    print(f"Error: |{sum(answers)} - {domainScore}| = {error}")
    return error
