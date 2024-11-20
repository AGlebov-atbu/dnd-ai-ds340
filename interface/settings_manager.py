import json
import os

SETTINGS_FILE = "user_settings.json"

def load_user_settings():
    """
        Load user settings from a JSON file.
    """
    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
    except FileNotFoundError:
        # Default settings.
        settings = {"fullscreen": False,
                    "language": "en"}
    return settings

def load_language(language):
    """
        Load translation file based on the selected language.
    """

    base_dir = os.path.dirname(__file__)
    language_dir = os.path.join(base_dir, "language")

    try:
        with open(os.path.join(language_dir, f"{language}.json"), "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Translation file for '{language}' not found. Defaulting to English.")
        with open(os.path.join(language_dir, "en.json"), "r", encoding="utf-8") as file:
            return json.load(file)

def save_user_settings(settings):
    """
        Save user settings to a JSON file.
    """
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)
