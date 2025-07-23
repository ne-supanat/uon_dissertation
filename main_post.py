import os
import sys

import stage_08_run_experiment_warning
import stage_09_visualisation_template_generation
import stage_10_visualisation_analysis

import display_progress
import paths

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
        print("\nRun 'main_post.py' to review the progress.")
        print("Run 'main_eval.py' to evaluate the result.")


def main(model_output_path: str, results_folder: str):
    results_path = results_folder
    os.makedirs(results_path, exist_ok=True)

    ## Ask to run experiment
    if not os.path.isfile(model_output_path):
        stage_08_run_experiment_warning.warn(model_output_path)
        sys.exit()
    else:
        # Display output file location
        display_progress.display_header()
        print(display_progress.model_output_progess(model_output_path))

    ## Visualisation template generation
    visualisation_template_think_path = os.path.join(
        results_path, paths.visualisation_template_think_file_path
    )
    visualisation_template_path = os.path.join(
        results_path, paths.visualisation_template_file_path
    )
    visualisations_path = os.path.join(results_path, paths.visualisation_directory_path)

    if not os.path.isfile(visualisation_template_path):
        stage_str = "Generate visualisation template script"
        proceed = ask_proceed(stage_str)
        if proceed:
            stage_09_visualisation_template_generation.generate(
                visualisations_path,
                model_output_path,
                visualisation_template_think_path,
                visualisation_template_path,
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
        results_path, paths.visualisation_analysis_file_path
    )

    if not os.path.isfile(visualisation_analysis_path):
        os.makedirs(visualisations_path, exist_ok=True)

        images = [image for image in os.listdir(visualisations_path)]

        size = len(images)
        if size > 0:
            print(
                f"\nFound {len(images)} item{'s' if size>1 else ''} at '{visualisations_path}'"
            )
            print(" , ".join(images))
        else:
            print(f"\nNo items found at '{visualisations_path}'.")
            print("Please create some visualisations first.\n")
            sys.exit()

        image_paths = [os.path.join(visualisations_path, image) for image in images]

        stage_str = "Generate visualisations analysis"
        proceed = ask_proceed(stage_str)
        if proceed:

            stage_10_visualisation_analysis.analyse(
                image_paths,
                visualisation_analysis_path,
            )

            print_end_stage(True)
            print()
        sys.exit()
    else:
        print(
            display_progress.visualisation_analysis_progess(visualisation_analysis_path)
        )
        print_end_stage(True)

    print()


if __name__ == "__main__":
    model_output_path = "./NetLogo Model/outputs.csv"
    results_folder = "results_4"

    # TODO: pick source & project from terminal
    main(model_output_path, results_folder)
