import os
from docx import Document


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
    doc_path = "data/travel_profile"
    txt_path = "data/travel_profile_txt"
    process_docx_table_to_txt(doc_path, txt_path)

    doc_path = "data/travel_scope"
    txt_path = "data/travel_scope_txt"
    process_docx_table_to_txt(doc_path, txt_path)
