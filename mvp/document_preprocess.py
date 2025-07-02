import os
import docx2txt
import re
from docx import Document


def read():
    source_path = "data/diary"
    filename = "ESM00385X1 W06w1.docx"
    content = docx2txt.process(f"{source_path}/{filename}")
    print(content[:50])
    print()


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
                f.writelines("\n".join(speaker_rows))


if __name__ == "__main__":
    doc_path = "data/diary"
    txt_path = "data/diary_txt"

    process_docx_to_txt(doc_path, txt_path)
