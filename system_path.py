import os
import json


class SystemPath:

    def __init__(self, name: str):
        self.project_name = name

    def get_00_project_path(self):
        return os.path.join(self.project_name, "00_project.json")

    def get_scope_data_directory_path(self):
        with open(self.get_00_project_path()) as f:
            data = json.loads(f.read())
        return data["scope"]

    def get_profile_data_directory_path(self):
        with open(self.get_00_project_path()) as f:
            data = json.loads(f.read())
        return data["profile"]

    def get_01_topic_path(self):
        return os.path.join(self.project_name, "01_topic.txt")

    def get_01_potential_outline_path(self):
        return os.path.join(self.project_name, "01_potential_outline.txt")

    def get_01_outline_path(self):
        return os.path.join(self.project_name, "01_outline.txt")

    def get_02_thematic_analysis_path(self):
        return os.path.join(self.project_name, "02_theme_codes.txt")

    def get_02_thematic_analysis_csv_path(self):
        return os.path.join(self.project_name, "02_theme_codes.csv")

    def get_02_eabss_scope_path(self):
        return os.path.join(self.project_name, "02_eabss_scope.txt")

    def get_03_eabss_main_actor_path(self):
        return os.path.join(self.project_name, "03_main_actor.txt")

    def get_03_eabss_usecase_diagram_path(self):
        return os.path.join(self.project_name, "03_diagram_usecase.txt")

    def get_03_eabss_class_diagram_path(self):
        return os.path.join(self.project_name, "03_diagram_class.txt")

    def get_03_eabss_activity_diagram_path(self):
        return os.path.join(self.project_name, "03_diagram_activity.txt")

    def get_03_eabss_state_diagram_path(self):
        return os.path.join(self.project_name, "03_diagram_state.txt")

    def get_03_eabss_interaction_diagram_path(self):
        return os.path.join(self.project_name, "03_diagram_interaction.txt")

    def get_04_archetypes_path(self):
        return os.path.join(self.project_name, "04_archetype.txt")

    def get_04_attributes_path(self):
        return os.path.join(self.project_name, "04_attribute.txt")

    def get_04_scenario_path(self):
        return os.path.join(self.project_name, "04_scenario.txt")

    def get_05_profiles_path(self):
        return os.path.join(self.project_name, "05_profiles.txt")

    def get_06_decision_archetype_path(self):
        return os.path.join(self.project_name, "06_decision_archetype.txt")

    def get_06_decision_profile_path(self):
        return os.path.join(self.project_name, "06_decision_profile.txt")

    def get_06_decision_probability_path(self):
        return os.path.join(self.project_name, "06_scenario_probability.txt")

    def get_07_simulation_script_think_path(self):
        return os.path.join(self.project_name, "07_simulation_script_think.txt")

    def get_07_simulation_script_path(self):
        return os.path.join(self.project_name, "07_simulation_script.txt")

    def get_visualisations_directory_path(self):
        return os.path.join(self.project_name, "visualisations")

    def get_09_visualisation_template_think_path(self):
        return os.path.join(self.project_name, "09_visualisation_template_think.txt")

    def get_09_visualisation_template_path(self):
        return os.path.join(self.project_name, "09_visualisation_template.txt")

    def get_10_visualisation_analysis_path(self):
        return os.path.join(self.project_name, "10_visualisation_analysis.txt")

    def get_eval_02_thematic_analysis_score_path(self):
        return os.path.join(self.project_name, "eval_02_thematic_analysis_score.csv")

    def get_eval_05_profile_score_path(self):
        return os.path.join(self.project_name, "eval_05_profile_quotes_score.csv")

    def get_eval_06_profile_scenario_answer_score_path(self):
        return os.path.join(self.project_name, "eval_06_scenario_answer_score.csv")


if __name__ == "__main__":
    path = SystemPath("travel2")
    print(path.get_scope_data_directory_path())
    print(path.get_profile_data_directory_path())
