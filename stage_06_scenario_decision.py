import numpy as np

import llm
from models.response_models import Profile, Scenario, ActionProbability
from models.archetypes import Archetype

import display_progress
from system_path import SystemPath

import json


def create_ground_truth(path: SystemPath):
    with open(path.get_04_archetypes_path(), "r") as f:
        archetypes = f.read().strip().splitlines()

    with open(path.get_04_scenario_path(), "r") as f:
        content = f.read()
        scenarios: list[Scenario] = [
            Scenario.model_validate_json(json.dumps(scenario_raw))
            for scenario_raw in json.loads(content)
        ]

    ground_truth = []
    for scenario in scenarios:
        response = generate_ground_truth(scenario)
        archetype_action_probs: list[ActionProbability] = response.parsed

        truth = {
            "scenario": scenario.scenario,
            "actions": scenario.actions,
            "archetype_action_probs": {},
        }

        for i, archetype in enumerate(archetypes):
            truth["archetype_action_probs"][archetype] = archetype_action_probs[i].probs

        ground_truth.append(truth)

    with open(path.get_06_scenario_ground_truth_path(), "w") as f:
        f.write(json.dumps(list(ground_truth), indent=4))

    print()
    print("-" * 50)
    print(
        f"Scenario ground truths saved to: '{path.get_06_scenario_ground_truth_path()}'\n"
    )


def generate_ground_truth(scenario: Scenario):
    prompt = f"""
Archetypes: 
{", ".join([type.value for type in Archetype])}

Scenario: {scenario.scenario}
Actions: {', '.join(scenario.actions)}

For each archetype, roleplay and give probability to each action base on archetype preference.
The total probability across all actions must equal to {1}

Example response:
[
  [Archetype1 Action1 Probability, Archetype1 Action2 Probability, Archetype1 Action3 Probability],
  [Archetype2 Action1 Probability, Archetype2 Action2 Probability, Archetype2 Action3 Probability],
  [Archetype3 Action1 Probability, Archetype3 Action2 Probability, Archetype3 Action3 Probability]
]
"""
    response = llm.generate_content(prompt, list[ActionProbability])
    return response


def create_profile_scenario_answers(path: SystemPath):
    with open(path.get_04_scenario_path(), "r") as f:
        content = f.read()
        scenarios: list[Scenario] = [
            Scenario.model_validate_json(json.dumps(scenario_raw))
            for scenario_raw in json.loads(content)
        ]

    with open(path.get_05_profiles_path(), "r") as f:
        content = f.read()
        profiles = [
            Profile.model_validate_json(profile)
            for profile in content.strip().split("\n\n")
        ]

    all_profile_answers = []
    for profile in profiles:
        # Generate all scenario answer
        profile_answers: list[ActionProbability] = generate_profile_scenario_answers(
            path, profile
        )

        profile_dict = {
            "file": profile.file,
            "archetype": profile.archetype.value,
            "scenarios": [],
        }

        for i, scenario in enumerate(scenarios):
            profile_dict["scenarios"].append(
                {
                    "scenario": scenario.scenario,
                    "actions": scenario.actions,
                    "action_probs": profile_answers[i].probs,
                }
            )

        all_profile_answers.append(profile_dict)

    with open(path.get_06_profile_scenario_answers_path(), "w") as f:
        f.write(json.dumps(all_profile_answers, indent=4))

        print()
    print("-" * 50)
    print(
        f"Profile scenario answers saved to: '{path.get_06_profile_scenario_answers_path()}'\n"
    )

    # TODO: (optional) save as csv as well
    # with open(path.get_06_profile_scenario_answers_path(), "w") as f:
    #     for profile in profiles:
    #         scenario_archetype_action_probs_list: list[ActionProbability] = (
    #             generate_profile_scenario_answers(path, profile)
    #         )

    #         for scenario_index, scenario_archetype_action_probs in enumerate(
    #             scenario_archetype_action_probs_list
    #         ):
    #             f.write(
    #                 f"{profile.file};{scenarios[scenario_index].scenario};{profile.archetype.value};"
    #             )
    #             f.write(
    #                 ";".join(
    #                     [str(prob) for prob in scenario_archetype_action_probs.probs]
    #                 )
    #             )
    #             f.write("\n")


def generate_profile_scenario_answers(
    path: SystemPath,
    profile: Profile,
) -> list[ActionProbability]:
    prompt = f"""
Based on this profile summary:
{profile.summary}

Profile attributes:
{"\n".join([f'{i+1}. {attribute}' for i,attribute in enumerate(profile.attributes)])}

Supporting quotes:
{"\n".join([f'{i+1}. {quote}' for i,quote in enumerate(profile.quotes)])}

Give probability to each action base on profile preference.
The total probability across all actions must equal to {1}

{display_progress.scenario_progess(path)}
"""
    response = llm.generate_content(prompt, list[ActionProbability])
    return response.parsed


def create_scenario_action_probability_table(path: SystemPath):
    # Fetch scenario questions
    with open(path.get_04_archetypes_path(), "r") as f:
        archetypes = f.read().strip().splitlines()

    with open(path.get_04_scenario_path(), "r") as f:
        content = f.read()
        scenarios: list[Scenario] = [
            Scenario.model_validate_json(json.dumps(scenario_raw))
            for scenario_raw in json.loads(content)
        ]

    scenario_answer_dict = convert_profile_answer_to_scenario_archetype_dict(path)

    scenario_probs = []
    for scenario in scenarios:
        scenario_prob = {
            "scenario": scenario.scenario,
            "actions": scenario.actions,
            "archetype_action_probs": {},
        }

        for archetype in archetypes:
            if archetype in scenario_answer_dict[scenario.scenario]:
                avg_probs = np.mean(
                    np.array(scenario_answer_dict[scenario.scenario][archetype]),
                    axis=0,
                )
                scenario_prob["archetype_action_probs"][archetype] = [
                    round(prob, 4) for prob in list(avg_probs)  # 4 decimal points
                ]

        scenario_probs.append(scenario_prob)

    print(scenario_probs)
    with open(path.get_06_decision_probability_path(), "w") as f:
        f.write(json.dumps(scenario_probs, indent=4))

    print()
    print("-" * 50)
    print(
        f"Decision probability table saved to: '{path.get_06_decision_probability_path()}'\n"
    )


def convert_profile_answer_to_scenario_archetype_dict(path: SystemPath):
    with open(path.get_06_profile_scenario_answers_path(), "r") as f:
        content = f.read()
        all_profile_scenario_answers = json.loads(content)

    # scenario_dict structure
    # {
    #     "scenario1": {
    #         "archetyp1": [
    #             [0.1, 0.2, 0.7],  # 1st profile with archetyp1's answer of scenario 1
    #             [0.1, 0.2, 0.7],  # 2nd profile with archetyp1's answer of scenario 1
    #             [0.1, 0.2, 0.7],  # 3rd profile with archetyp1's answer of scenario 1
    #         ],
    #         "archetyp2": [
    #             [0.1, 0.2, 0.7],  # 1st profile with archetyp2's answer of scenario 1
    #             [0.1, 0.2, 0.7],  # 2nd profile with archetyp2's answer of scenario 1
    #             [0.1, 0.2, 0.7],  # 3rd profile with archetyp2's answer of scenario 1
    #         ],
    #     }
    # }

    scenario_answer_dict = {}
    for profile_scenario_answer_dict in all_profile_scenario_answers:
        archetype_key = profile_scenario_answer_dict["archetype"]
        answer_sceanarios = profile_scenario_answer_dict["scenarios"]
        for answer_sceanario in answer_sceanarios:
            scenario_key = answer_sceanario["scenario"]

            if scenario_key not in scenario_answer_dict:
                scenario_answer_dict[scenario_key] = {}

            if archetype_key not in scenario_answer_dict[scenario_key]:
                scenario_answer_dict[scenario_key][archetype_key] = []

            scenario_answer_dict[scenario_key][archetype_key].append(
                answer_sceanario["action_probs"]
            )

    return scenario_answer_dict


def create_decision_probability_table_from_ground_truth(path: SystemPath):
    # Copy ground truth to decision probabilities file
    with open(path.get_06_scenario_ground_truth_path(), "r") as f:
        content = f.read()

    with open(path.get_06_decision_probability_path(), "w") as f:
        f.write(content)

    print()
    print("-" * 50)
    print(
        f"Decision probability table saved to: '{path.get_06_decision_probability_path()}'\n"
    )


if __name__ == "__main__":
    path = SystemPath("travel")

    ## Create decision probability using ground truth (roleplay as archetype)
    # create_ground_truth(path)
    # create_decision_probability_table_from_ground_truth(path)

    ## Create decision probability using roleplay as profile
    # create_profile_scenario_answers(path)
    create_scenario_action_probability_table(path)
