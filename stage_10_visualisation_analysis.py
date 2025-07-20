import os
import llm


def analyse(
    images_paths,
    visualisation_analysis_path,
):
    response = generate_explanation(images_paths)
    with open(visualisation_analysis_path, "w") as f:
        f.write(response.text)

    print(
        f"\nVisualisation analysis result saved to: '{visualisation_analysis_path}'\n"
    )


def generate_explanation(images_paths):
    prompt = f"""
These images are result from simulation experiments.
What are the findings of these images? Can you summarise the explanation?
"""

    response = llm.generate_content_from_images(images_paths, prompt)
    return response


if __name__ == "__main__":
    results_path = "results_2"

    images_paths = [
        os.path.join(results_path, path) for path in ["plot_25.png", "plot_75.png"]
    ]

    visualisation_analysis_path = os.path.join(
        results_path, "final_analysis_explanation.txt"
    )
    analyse(
        images_paths,
        visualisation_analysis_path,
    )
