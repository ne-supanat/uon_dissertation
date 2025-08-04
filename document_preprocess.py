import os
import re
from docx import Document


def process_docx_to_txt(source_path, destination_path):
    for filename in os.listdir(source_path):
        if filename.endswith(".docx"):
            doc = Document(f"{source_path}/{filename}")

            speaker_rows = []

            for para in doc.paragraphs[:]:
                row = para.text.strip()
                if row == "":
                    continue
                # Remove participant ID eg. E01, S01, W01
                elif re.match(r"^[ESW][0-9]{2}$", row):
                    continue
                # Remove Total Page at the end
                elif re.match(r"^[0-9]+", row):
                    continue
                # Remove non-conversation parts eg. [laugh], [do a survey]
                elif re.match(r"^\[.*\]$", row):
                    continue

                # print(para.text)
                # print(para.runs[0].bold)
                speaker_rows.append(
                    f'{"Interviewer" if para.runs[0].bold else "Participant"}: {row}'
                )

            # Write content with speaker on txt file
            name = filename.split(".")[0]
            with open(f"{destination_path}/{name}.txt", "w") as f:
                f.writelines("\n".join(speaker_rows).replace("  ", " "))


def process_docx_table_to_txt(source_path, destination_path):
    os.makedirs(destination_path, exist_ok=True)
    for filename in os.listdir(source_path):
        if filename.endswith(".docx"):
            doc = Document(f"{os.path.join(source_path,filename)}")

            speaker_rows = []

            for table in doc.tables:
                for row in table.rows:
                    speaker_rows.append(
                        f"{row.cells[0].text}: {row.cells[1].text.replace("\n"," ")}"
                    )

            name = filename.split(".")[0]
            with open(f"{os.path.join(destination_path,name)}.txt", "w") as f:
                f.writelines("\n".join(speaker_rows).replace("  ", " "))


if __name__ == "__main__":
    # doc_path = "data/diary"
    # txt_path = "data/diary_txt"
    # process_docx_to_txt(doc_path, txt_path)

    doc_path = "data/travel_profile"
    txt_path = "data/travel_profile_txt"
    process_docx_table_to_txt(doc_path, txt_path)

    doc_path = "data/travel_scope"
    txt_path = "data/travel_scope_txt"
    process_docx_table_to_txt(doc_path, txt_path)
