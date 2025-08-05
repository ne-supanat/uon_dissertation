import os
import llm

from system_path import SystemPath
from models.response_models import VisualisationAnalysisResponse


def analyse_visualisations(path: SystemPath, images: list[str]):
    image_paths = [
        os.path.join(path.get_visualisations_directory_path(), image)
        for image in images
    ]

    response = generate_visualisations_explanation(image_paths)
    with open(path.get_10_visualisation_analysis_path(), "w") as f:
        f.write(response.text)

    print()
    print("-" * 50)
    print(
        f"Visualisation analysis result saved to: '{path.get_10_visualisation_analysis_path()}'\n"
    )


def generate_visualisations_explanation(image_paths):
    prompt = f"""
These images are result from simulation experiments.
What are the findings of these images? Can you summarise the explanation?
"""

    response = llm.generate_content_from_images(
        image_paths, prompt, VisualisationAnalysisResponse
    )
    return response


if __name__ == "__main__":
    path = SystemPath("results_travel_1")
    analyse_visualisations(path, ["transport_usage.png"])
