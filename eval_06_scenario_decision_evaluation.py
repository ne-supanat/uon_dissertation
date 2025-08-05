import json
import numpy as np
import scipy.stats as stats

from system_path import SystemPath
from sklearn.metrics import mean_squared_error
from stage_06_scenario_decision import convert_profile_answer_to_scenario_archetype_dict
from models.response_models import Scenario


def evaluate(path: SystemPath):
    calculate_mse_decision_probability_to_ground_truth(path)
    print()


def calculate_mse_decision_probability_to_ground_truth(path: SystemPath):
    with open(path.get_06_scenario_ground_truth_path(), "r") as f:
        ground_truth = json.loads(f.read())

    with open(path.get_06_decision_probability_path(), "r") as f:
        decision_probability = json.loads(f.read())

    # MSE between (synthesised) ground truth & profile's decision probability
    ref_probs = []
    cand_probs = []
    for i, ref_scenario in enumerate(ground_truth):
        cand_scenario = decision_probability[i]

        for archetype, ref_action_probs in ref_scenario[
            "archetype_action_probs"
        ].items():
            if archetype in cand_scenario["archetype_action_probs"]:
                ref_probs += ref_action_probs
                cand_probs += cand_scenario["archetype_action_probs"][archetype]

    print(f"MSE between ground truth & profile's decision probability:")
    print(f"{mean_squared_error(ref_probs, cand_probs):.4f}")


def calculate_mse_archetype_answer_to_ground_truth(path: SystemPath):
    with open(path.get_06_profile_scenario_answers_path(), "r") as f:
        profile_scenario_answers = json.loads(f.read())

    with open(path.get_06_scenario_ground_truth_path(), "r") as f:
        ground_truth = json.loads(f.read())

    mse_scenarios = []
    for profile in profile_scenario_answers:
        for i, scenario in enumerate(profile["scenarios"]):
            cand_probs = scenario["action_probs"]
            ref_probs = ground_truth[i]["archetype_action_probs"][profile["archetype"]]
            mse_scenarios.append(mean_squared_error(ref_probs, cand_probs))

    print(f"Mean ± Std of MSE between ground truth & profile's scenario answers:")
    print(f"{np.mean(mse_scenarios):.4f} ± {np.std(mse_scenarios):.4f}")


def calculate_std_profile_answer_by_archetype(path: SystemPath):
    with open(path.get_04_archetypes_path(), "r") as f:
        archetypes = f.read().strip().splitlines()

    with open(path.get_04_scenario_path(), "r") as f:
        content = f.read()
        scenarios: list[Scenario] = [
            Scenario.model_validate_json(json.dumps(scenario_raw))
            for scenario_raw in json.loads(content)
        ]

    scenario_answer_dict = convert_profile_answer_to_scenario_archetype_dict(path)

    stds = []
    for scenario in scenarios:
        for archetype in archetypes:
            if archetype in scenario_answer_dict[scenario.scenario]:
                std = np.std(
                    np.array(scenario_answer_dict[scenario.scenario][archetype]),
                    axis=0,
                )

                stds += list(std)

    print(f"Mean Standard Deviation of each action probability in every scenario:")
    print(f"{np.mean(stds):.4f}")


if __name__ == "__main__":
    path = SystemPath("travel")
    evaluate(path)
