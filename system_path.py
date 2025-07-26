import os


class SystemPath:

    def __init__(self, name: str):
        self.project_name = name

    def get_01_objective_path(self):
        return os.path.join(self.project_name, "01_objective.txt")

    def get_02_thematic_analysis_path(self):
        return os.path.join(self.project_name, "02_thematic_analysis_codes.txt")

    def get_02_thematic_analysis_csv_path(self):
        return os.path.join(self.project_name, "02_thematic_analysis_codes.csv")

    def get_02_eabss_scope_path(self):
        return os.path.join(self.project_name, "02_eabss_scope.txt")

    def get_03_eabss_usecase_diagram_path(self):
        return os.path.join(self.project_name, "03_eabss_diagram_usecase_diagram.txt")

    def get_03_eabss_class_diagram_path(self):
        return os.path.join(self.project_name, "03_eabss_diagram_class_diagram.txt")

    def get_03_eabss_activity_diagram_path(self):
        return os.path.join(self.project_name, "03_eabss_diagram_activity_diagram.txt")

    def get_03_eabss_state_diagram_path(self):
        return os.path.join(self.project_name, "03_eabss_diagram_state_diagram.txt")

    def get_03_eabss_interaction_diagram_path(self):
        return os.path.join(
            self.project_name, "03_eabss_diagram_interaction_diagram.txt"
        )

    def get_04_archetypes_path(self):
        return os.path.join(self.project_name, "04_archetype.txt")

    def get_04_attributes_path(self):
        return os.path.join(self.project_name, "04_attribute.txt")

    def get_04_scenario_questions_path(self):
        return os.path.join(self.project_name, "04_scenario_questions.txt")

    def get_04_scenario_choices_path(self):
        return os.path.join(self.project_name, "04_scenario_choices.txt")

    def get_05_profiles_path(self):
        return os.path.join(self.project_name, "05_profiles.txt")

    def get_06_profile_scenario_answers_path(self):
        return os.path.join(self.project_name, "06_profile_scenario_answers.csv")

    def get_06_decision_probability_path(self):
        return os.path.join(self.project_name, "06_scenario_probability.csv")

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

    def get_eval_06_scenario_ground_truth_path(self):
        return os.path.join(self.project_name, "eval_06_scenario_ground_truth.txt")

    def get_eval_06_profile_scenario_answer_score_path(self):
        return os.path.join(self.project_name, "eval_06_scenario_answer_score.csv")
