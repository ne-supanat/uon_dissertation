import os
import json
from system_path import SystemPath


def run_setup_project(path: SystemPath):
    # Create project directory
    os.makedirs(path.project_name, exist_ok=True)

    # Setup source data paths
    while True:
        source_scope_directory = input("Enter path to dataset for scope: ")
        if os.path.isdir(source_scope_directory):
            break
        print("Directory not found. Please try again.")

    while True:
        source_profile_directory = input("Enter path to dataset for profile: ")
        if os.path.isdir(source_profile_directory):
            break
        print("Directory not found. Please try again.")

    with open(path.get_00_project_path(), "w") as f:
        dict = {
            "scope": source_scope_directory,
            "profile": source_profile_directory,
        }
        f.write(json.dumps(dict, indent=4))


if __name__ == "__main__":
    run_setup_project("travel")
