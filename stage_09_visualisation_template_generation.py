import os
import pandas as pd
import llm
from models.response_models import ThinkScriptResponse
import plotly.express as px


def generate(
    visualisations_path,
    model_output_path,
    output_analysis_think_path,
    output_analysis_path,
):

    df = pd.read_csv(model_output_path)
    example_df = str(df.head())

    response = generate_script(visualisations_path, example_df)

    with open(output_analysis_think_path, "w") as f:
        f.write(response.think)
    with open(output_analysis_path, "w") as f:
        f.write(response.script)

    print()
    print("-" * 50)
    print(
        f"Visualisation template script reasoning result saved to: '{output_analysis_think_path}'"
    )
    print(f"Visualisation template script result saved to: '{output_analysis_path}'")
    print(
        f"\nPlease use the generated template to create some visualisations at '{visualisations_path}'."
    )
    print(f"Don't forget to update the Visualisation title to match the scenario.")


def generate_script(visualisation_folder_path, example_df) -> ThinkScriptResponse:
    prompt = f"""
And example data from './NetLogo Model/outputs.csv':

{example_df}

Generate python script for visualisation using plotly.

{"-"*50}
Follow this NetLogo template:

import pandas as pd

df = pd.read_csv('./NetLogo Model/outputs.csv')
# Visualise data in df

# Save visualisation image in folder visualisations
os.makedirs("{visualisation_folder_path}", exist_ok=True)

{"-"*50}
"""

    response = llm.generate_content(prompt, ThinkScriptResponse).parsed
    return response


if __name__ == "__main__":
    model_output_path = "./NetLogo Model/outputs_25.csv"

    results_path = "results_2"
    output_analysis_think_path = os.path.join(
        results_path, "output_analysis_script_think.txt"
    )
    output_analysis_path = os.path.join(results_path, "output_analysis_script.txt")

    generate(
        results_path,
        model_output_path,
        output_analysis_think_path,
        output_analysis_path,
    )
