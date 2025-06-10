import pandas as pd
import os

path = f"data/DAICWOZ"
pathCSV = path + "/csv"
pathTXT = path + "/txt"
os.makedirs(pathTXT, exist_ok=True)

for csvFile in os.listdir(pathCSV):
    csvFilePath = f"{pathCSV}/{csvFile}"
    print(csvFilePath)

    newPath = f"{pathTXT}/{csvFile.split('.')[0]}.txt"
    print(newPath)

    with open(newPath, "w+") as f:
        df = pd.read_csv(csvFilePath, delimiter="\t")
        df["transcript"] = df["speaker"] + ": " + df["value"]

        for value in df["transcript"].tolist():
            f.write(value + "\n")
