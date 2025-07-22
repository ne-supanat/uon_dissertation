def warn(
    model_output_path,
):
    print(f"\nNo existing output found at '{model_output_path}'")
    print("Please run an experiment first.")
    print("Note: output must be in CSV format")


if __name__ == "__main__":
    model_output_path = "./NetLogo Model/outputs.csv"
    warn(model_output_path)
