import unittest

import answer_evaluation as ans_eval


class TestProfileValidation(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")


class TestAnswerEvaluation(unittest.TestCase):
    def testEvaluateLabelQuestion(self):
        # questions: list[dict]
        # domainLabel: str
        # answers: list[str]

        # Free selected items range
        questions = [
            {
                "question": "select items",
                "choices": ["Thailand", "Spain", "Singapore", "England", "Norway"],
                "choice_values": [
                    "fav_warm",
                    "fav_warm",
                    "fav_warm",
                    "fav_cold",
                    "fav_cold",
                ],
            }
        ]

        # 1 item - 100% correct case
        self.assertEqual(
            ans_eval.evaluateLabelQuestions(questions, "fav_warm", [["Thailand"]]),
            1.0,
        )

        # 2 item - 100% correct case
        self.assertEqual(
            ans_eval.evaluateLabelQuestions(
                questions, "fav_warm", [["Thailand", "Spain"]]
            ),
            1.0,
        )

        # 2 item - 50% correct case
        self.assertEqual(
            ans_eval.evaluateLabelQuestions(
                questions, "fav_warm", [["Singapore", "Norway"]]
            ),
            0.5,
        )

        # 2 item - 0% correct case
        self.assertEqual(
            ans_eval.evaluateLabelQuestions(
                questions, "fav_warm", [["England", "Norway"]]
            ),
            0,
        )

        # 0 item - select 0 item case
        # TODO: choose new metric
        self.assertEqual(
            ans_eval.evaluateLabelQuestions(questions, "fav_warm", [[]]),
            0,
        )

        # Error - select duplicate items
        with self.assertRaises(Exception):
            ans_eval.evaluateLabelQuestions(
                questions, "fav_warm", [["Thailand", "Thailand"]]
            ),

        # Error - item not in choices case
        with self.assertRaises(Exception):
            ans_eval.evaluateLabelQuestions(questions, "fav_warm", [["test"]]),

        # Specific selected items range
        questions = [
            {
                "question": "select 2 items",
                "choices": ["Thailand", "Spain", "Singapore", "England", "Norway"],
                "choice_values": [
                    "fav_warm",
                    "fav_warm",
                    "fav_warm",
                    "fav_cold",
                    "fav_cold",
                ],
            }
        ]

        # Correct case
        self.assertEqual(
            ans_eval.evaluateLabelQuestions(
                questions, "fav_warm", [["Thailand", "Spain"]]
            ),
            1.0,
        )

        # Error - select less than asked
        with self.assertRaises(Exception):
            ans_eval.evaluateLabelQuestions(questions, "fav_warm", [["Thailand"]]),

        # Error - select more than asked
        with self.assertRaises(Exception):
            ans_eval.evaluateLabelQuestions(
                questions, "fav_warm", [["Thailand", "Spain", "Singapore"]]
            ),

        # Several questions
        questions = [
            {
                "question": "Pick countries you want to go?",
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
                "question": "Pick activities you want to do?",
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

        # Correct case
        self.assertEqual(
            ans_eval.evaluateLabelQuestions(
                questions,
                "fav_warm",
                [
                    ["Thailand", "Spain"],
                    ["Scuba Diving", "Swimming"],
                ],
            ),
            1.0,
        )

        # Error - number of questions and answers not equal case
        with self.assertRaises(Exception):
            ans_eval.evaluateLabelQuestions(
                questions, "fav_warm", [["Thailand", "Spain"]]
            ),

    def testEvaluateScoreQuestion(self):
        # domainScore: float
        # answers: list[float]

        # Free selected items range
        questions = [
            "You love warm countries",
            "You love summer season",
            "You like rain and snow",
        ]

        # Normal case
        self.assertEqual(
            ans_eval.evaluateScoreQuestions(10, [5, 5, 1]),
            1.0,
        )

        self.assertEqual(
            ans_eval.evaluateScoreQuestions(10, [5, 2, 1]),
            2.0,
        )


if __name__ == "__main__":
    unittest.main()
