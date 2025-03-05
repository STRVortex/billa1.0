import os
import yaml

languages = {}
languages_present = {}

# Load language files
for filename in os.listdir(r"./strings/langs/"):
    if "en" not in languages:
        languages["en"] = yaml.safe_load(
            open(r"./strings/langs/en.yml", encoding="utf8")
        )
        languages_present["en"] = languages["en"].get("name", "English")

    if filename.endswith(".yml"):
        language_name = filename[:-4]  # Extract language code from filename
        if language_name == "en":
            continue

        languages[language_name] = yaml.safe_load(
            open(r"./strings/langs/" + filename, encoding="utf8")
        )

        # Ensure all keys from English are present in the other language files
        for item in languages["en"]:
            if item not in languages[language_name]:
                languages[language_name][item] = languages["en"][item]

        # Store language name safely
        try:
            languages_present[language_name] = languages[language_name].get("name", language_name)
        except Exception as e:
            print(f"There is some issue with the language file: {filename}")
            exit()


def get_string(lang: str):
    """Retrieve the language dictionary. Fallback to English if the language is missing."""
    return languages.get(lang, languages["en"])
