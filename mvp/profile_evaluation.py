from response_models import Profile


def evaluate(profiles_path: str):
    with open(profiles_path, "r") as f:
        content = f.read()

    profiles: list[Profile] = [
        Profile.model_validate_json(p) for p in content.strip().split("\n\n")
    ]

    not_found_dict = {}
    for profile in profiles:
        with open(profile.file, "r") as f:
            lines = f.read().strip().split("\n")

        not_found_dict[profile.file] = []
        for quote in profile.quotes:
            found = False
            for line in lines:
                if quote in line and line.startswith("Participant: "):
                    found = True

            if not found:
                not_found_dict[profile.file].append(quote)

    print("- NOT FOUND QUOTES -")
    print(not_found_dict)


if __name__ == "__main__":
    profiles_path = "mvp/results/profiles.txt"
    evaluate(profiles_path)
