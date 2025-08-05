import os


def get_transcript_file_paths(source_directory):
    return [
        f"{os.path.join(source_directory, filename)}"
        for filename in sorted(os.listdir(source_directory))
        if filename.endswith(".txt")
    ]
