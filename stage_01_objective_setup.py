import json
from google.genai.types import GenerateContentResponse

from system_path import SystemPath
import llm
from models.response_models import OutlineResponse


def setup_topic(path: SystemPath):
    print(
        "Please Enter a brief description of the study topic (you may include context and goal):"
    )
    input_topic = input()

    with open(path.get_01_topic_path(), "w") as f:
        f.write(input_topic)

    print()
    print("-" * 50)
    print(f"Topic saved to: '{path.get_01_topic_path()}'")


def setup_outline(path: SystemPath):
    with open(path.get_01_topic_path(), "r") as f:
        topic = f.read()

    response = generate_potential_outline(topic)
    outline: OutlineResponse = response.parsed

    print("Please enter the following project outline components:")

    print()
    print("Potential model's Objective")
    for objective in outline.objective:
        print(f" - {objective}")
    print()

    input_objective = input("Enter model's Objecttive: ")

    print()
    print("Potential model's Experimental Factors (Inputs):")
    for outline_input in outline.input:
        print(f" - {outline_input}")
    print()

    input_experiment_factor = input("Enter model's Experimental Factors (Inputs)")

    print()
    print("Potential model's Responses (Outputs):")
    for output in outline.output:
        print(f" - {output}")
    print()

    input_response = input("Enter model's Responses (Outputs)")

    with open(path.get_01_outline_path(), "w") as f:
        dict = {
            "objective": input_objective,
            "input": input_experiment_factor,
            "output": input_response,
        }
        f.write(json.dumps(dict, indent=4))

    print()
    print("-" * 50)
    print(f"Result saved to: '{path.get_01_outline_path()}'")


def generate_potential_outline(
    topic: str,
) -> GenerateContentResponse:

    prompt = f"""
Based simulation Topic, Context, Goal is
{topic}

Please suggest potential Objective, Experiment factor (input), Response (output) of the model.
Give me {3} potential element each.
"""
    response = llm.generate_content(
        prompt,
        response_schema=OutlineResponse,
    )
    return response


if __name__ == "__main__":
    path = SystemPath("results_4")
    setup_topic(path)
    setup_outline(path)
