import json

from system_path import SystemPath
from sklearn.metrics import mean_squared_error


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
    for i in range(len(ground_truth)):
        cand_scenario = decision_probability[i]
        ref_scenario = ground_truth[i]

        for archetype, ref_action_probs in ref_scenario[
            "archetype_action_probs"
        ].items():
            if archetype in cand_scenario["archetype_action_probs"]:
                ref_probs += ref_action_probs
                cand_probs += cand_scenario["archetype_action_probs"][archetype]

    print(f"MSE between ground truth & profile's decision probability:")
    print(f"{mean_squared_error(ref_probs, cand_probs):.4f}")


if __name__ == "__main__":
    path = SystemPath("travel")
    evaluate(path)
