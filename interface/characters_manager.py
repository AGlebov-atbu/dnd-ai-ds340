import json

CHARACTERS_FILE = "user_characters.json"

class Character:
    def __init__(self, cid, name, age, positive_traits, negative_traits, lore):
        self.cid = cid
        self.name = name
        self.age = age
        self.positive_traits = positive_traits
        self.negative_traits = negative_traits
        self.lore = lore

def load_user_characters():
    """Load characters from a JSON file."""
    try:
        with open(CHARACTERS_FILE, "r") as file:
            characters_data = json.load(file)
            # Make Character objects from dictionaries.
            return [
                Character(**char) if isinstance(char, dict) else char
                for char in characters_data
            ]
    except FileNotFoundError:
        return []


def save_user_characters(characters):
    """Save characters to a JSON file."""
    with open(CHARACTERS_FILE, "w") as file:
        # Transfer Character objects only.
        json.dump([char.__dict__ if hasattr(char, "__dict__") else char for char in characters], file)

def get_last_cid():
    """Return the highest cid used or -1 if no characters exist."""
    try:
        with open(CHARACTERS_FILE, "r") as file:
            characters_data = json.load(file)
            if not characters_data:
                return -1  # If the list is empty.
            return max(char["cid"] for char in characters_data)
    except (FileNotFoundError, json.JSONDecodeError):
        return -1  # If file does not exist.
