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
            # Преобразуем в объекты, если это словари
            return [
                Character(**char) if isinstance(char, dict) else char
                for char in characters_data
            ]
    except FileNotFoundError:
        return []


def save_user_characters(characters):
    """Save characters to a JSON file."""
    with open(CHARACTERS_FILE, "w") as file:
        # Проверяем, объекты ли это или словари, и преобразуем только объекты.
        json.dump([char.__dict__ if hasattr(char, "__dict__") else char for char in characters], file)

