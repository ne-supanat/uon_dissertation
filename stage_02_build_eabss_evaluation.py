import csv


def evaluate(ta_codes_csv_path: str):
    # check quoute are in its file
    with open(ta_codes_csv_path) as fcsv:
        reader = csv.reader(fcsv, delimiter=";")
        next(reader, None)

        file = ""
        lines = []  # transcript lines
        not_found_dict = {}
        for row in reader:
            # row[0] quote file
            # if it new file change transcript lines
            if file != row[0]:
                file = row[0]
                with open(row[0], "r") as f:
                    lines = f.read().strip().split("\n")

                if file not in not_found_dict:
                    not_found_dict[file] = []

            quote = row[-1]
            found = False
            for line in lines:
                if quote in line and line.startswith("Participant: "):
                    found = True

            if not found:
                not_found_dict[file].append(quote)

    print("- NOT FOUND QUOTES -")
    print(not_found_dict)


if __name__ == "__main__":
    document_paths = ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    ta_codes_csv_path = "results/thematic_analysis_codes.csv"
    evaluate(ta_codes_csv_path)
