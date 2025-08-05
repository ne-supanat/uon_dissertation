import pandas as pd
import llm
from models.response_models import ThinkScriptResponse
import plotly.express as px

from system_path import SystemPath


def build_visualisation_template(path: SystemPath, model_output_path: str):

    df = pd.read_csv(model_output_path)
    example_df = str(df.head())

    response = generate_visualisation_template_script(path, example_df)

    with open(path.get_09_visualisation_template_think_path(), "w") as f:
        f.write(response.think)
    with open(path.get_09_visualisation_template_path(), "w") as f:
        f.write(response.script)

    print()
    print("-" * 50)
    print(
        f"Visualisation template script reasoning result saved to: '{path.get_09_visualisation_template_think_path()}'"
    )
    print(
        f"Visualisation template script result saved to: '{path.get_09_visualisation_template_path()}'"
    )
    print(
        f"\nPlease use the generated template to create some visualisations at '{path.get_visualisations_directory_path()}'."
    )
    print(f"Don't forget to update the Visualisation title to match the scenario.")


def generate_visualisation_template_script(
    path: SystemPath,
    example_df,
) -> ThinkScriptResponse:
    prompt = f"""
An example data from './NetLogo Model/outputs.csv':

{example_df}

Generate python script for visualisation using plotly.

{"-"*50}
Follow this template:

import pandas as pd

df = pd.read_csv('./NetLogo Model/outputs.csv')
# Visualise data in df

# Save visualisation image in folder visualisations
os.makedirs("{path.get_visualisations_directory_path()}", exist_ok=True)

{"-"*50}
"""

    response = llm.generate_content(prompt, ThinkScriptResponse).parsed
    return response


if __name__ == "__main__":
    path = SystemPath("travel")
    model_output_path = "./NetLogo Model/outputs.csv"

    build_visualisation_template(path, model_output_path)
