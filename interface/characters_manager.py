import json

CHARACTERS_FILE = "user_characters.json"

class Character:
    def __init__(self, name, age, positive_traits, negative_traits, lore):
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
            # Transform into characters objects.
            return [Character(**char) for char in characters_data]
    except FileNotFoundError:
        # Default: there are no characters (yet).
        return []

def save_user_characters(characters):
    """Save characters to a JSON file."""
    with open(CHARACTERS_FILE, "w") as file:
        json.dump([char.__dict__ for char in characters], file)
