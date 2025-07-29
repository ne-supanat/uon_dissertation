import argparse
import os
import sys

import stage_08_run_experiment_warning
import stage_09_visualisation_template_generation
import stage_10_visualisation_analysis

import display_progress
from system_path import SystemPath

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


def run_analysis_warning(model_output_path: str):
    if not os.path.isfile(model_output_path):
        stage_08_run_experiment_warning.warn(model_output_path)
        sys.exit()
    else:
        # Display output file location
        display_progress.display_header()
        print(display_progress.model_output_progess(model_output_path))


def run_build_visualisation_template(path: SystemPath):
    if not os.path.isfile(path.get_09_visualisation_template_path()):
        stage_str = "Build visualisation template"
        proceed = ask_proceed(stage_str)
        if proceed:
            stage_09_visualisation_template_generation.build_visualisation_template(
                path, model_output_path
            )

            print_end_stage()
        sys.exit()
    else:
        print(display_progress.visualisation_template_progess(path))


def run_analyse_visualisations(path: SystemPath):
    if not os.path.isfile(path.get_10_visualisation_analysis_path()):

        visualisations_directory_path = path.get_visualisations_directory_path()
        os.makedirs(visualisations_directory_path, exist_ok=True)

        images = [image for image in os.listdir(visualisations_directory_path)]

        size = len(images)
        if size > 0:
            print(
                f"\nFound {len(images)} item{'s' if size>1 else ''} at '{visualisations_directory_path}'"
            )
            print(" , ".join(images))
        else:
            print(f"\nNo items found at '{visualisations_directory_path}'.")
            print("Please create some visualisations first.\n")
            sys.exit()

        stage_str = "Analyse visualisations"
        proceed = ask_proceed(stage_str)
        if proceed:

            stage_10_visualisation_analysis.analyse_visualisations(path, images)

            print_end_stage(True)
    else:
        print(display_progress.visualisation_analysis_progess(path))
        print_end_stage(True)


def main(project_name: str, model_output_path: str):
    os.makedirs(project_name, exist_ok=True)

    path = SystemPath(project_name)

    # Stage 08 Ask to run experiment
    run_analysis_warning(model_output_path)

    # Stage 09 Visualisation template generation
    run_build_visualisation_template(path)

    # Stage 10 Visualisations Analysis
    run_analyse_visualisations(path)

    print()


if __name__ == "__main__":
    model_output_path = "./NetLogo Model/outputs.csv"

    parser = argparse.ArgumentParser("Main System")
    parser.add_argument("project_name", help="A project name", type=str)

    args = parser.parse_args()
    main(args.project_name, model_output_path)
