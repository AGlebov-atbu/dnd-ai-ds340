import json

SETTINGS_FILE = "user_settings.json"

def load_user_settings():
    """
        Load user settings from a JSON file.
    """
    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
    except FileNotFoundError:
        settings = {"fullscreen": False}  # Default settings
    return settings

def save_user_settings(settings):
    """
        Save user settings to a JSON file.
    """
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)
