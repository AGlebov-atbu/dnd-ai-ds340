import json

CHARACTERS_FILE = "user_characters.json"

def load_user_characters():
    """
        Load user settings from a JSON file.
    """
    try:
        with open(CHARACTERS_FILE, "r") as file:
            characters = json.load(file)
    except FileNotFoundError:
        characters = {"characters_number": 0}
    return characters

def save_user_characters(characters):
    """
        Save user characters to a JSON file.
    """
    with open(CHARACTERS_FILE, "w") as file:
        json.dump(characters, file)
