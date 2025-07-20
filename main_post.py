import os
import sys

import stage_09_visualisation_template_generation
import stage_10_visualisation_analysis

import display_progress

# TODO: add comments


def ask_proceed(stage_str: str) -> bool:
    approve = None
    while approve not in ["y", "n"]:
        approve = input(f"\nProceed to next stage: {stage_str}? (y/n): ").lower()
    return approve == "y"


def print_end_stage(is_last_stage: bool = False):
    if not is_last_stage:
        print("\nRun 'python main_post.py' to continue to the next stage.\n")
    else:
        print("-" * 50 + "\nAll post process stages completed\n" + "=" * 50)


def main(model_output_path: str, results_folder: str):
    results_path = results_folder
    os.makedirs(results_path, exist_ok=True)

    ## Ask to run experiment
    if not os.path.isfile(model_output_path):
        print(f"\nNo existing output found at '{model_output_path}'")
        print("Please run an experiment first.")
        print("Note: output must be in CSV format")
        sys.exit()
    else:
        # Display output file location
        display_progress.display_header()
        print(display_progress.model_output_progess(model_output_path))

    ## Visualisation template generation
    visualisation_template_think_path = os.path.join(
        results_path, "visualisation_template_think.txt"
    )
    visualisation_template_path = os.path.join(
        results_path, "visualisation_template.txt"
    )

    if not os.path.isfile(visualisation_template_path):
        stage_str = "Generate visualisation template script"
        proceed = ask_proceed(stage_str)
        if proceed:
            stage_09_visualisation_template_generation.generate(
                results_path,
                model_output_path,
                visualisation_template_think_path,
                visualisation_template_path,
            )

            print(
                display_progress.visualisation_template_progess(
                    visualisation_template_think_path,
                    visualisation_template_path,
                )
            )
            print_end_stage()
        sys.exit()
    else:
        print(
            display_progress.visualisation_template_progess(
                visualisation_template_think_path,
                visualisation_template_path,
            )
        )

    ## Visualisations Analysis
    visualisation_analysis_path = os.path.join(
        results_path, "visualisation_analysis.txt"
    )

    if not os.path.isfile(visualisation_analysis_path):
        visualisations_path = os.path.join(results_path, "visualisations")

        os.makedirs(visualisations_path, exist_ok=True)
        image_paths = [
            os.path.join(visualisations_path, path)
            for path in os.listdir(visualisations_path)
        ]

        size = len(image_paths)
        if size > 0:
            print(
                f"\nFound {len(image_paths)} item{'s' if size>1 else ''} at '{visualisations_path}'"
            )
        else:
            print(f"\nNo items found at '{visualisation_analysis_path}'.")
            print("Please create some visualisations first before the analysis.\n")
            sys.exit()

        print(image_paths)

        stage_str = "Generate visualisations analysis"
        proceed = ask_proceed(stage_str)
        if proceed:

            stage_10_visualisation_analysis.analyse(
                image_paths,
                visualisation_analysis_path,
            )

            print(
                display_progress.visualisation_analysis_progess(
                    visualisation_analysis_path
                )
            )
            print_end_stage(True)
        sys.exit()
    else:
        print(
            display_progress.visualisation_analysis_progess(visualisation_analysis_path)
        )
        print_end_stage(True)

    print()


if __name__ == "__main__":
    model_output_path = "./NetLogo Model/outputs.csv"
    results_folder = "results_2"

    # TODO: pick source & project from terminal
    main(model_output_path, results_folder)
