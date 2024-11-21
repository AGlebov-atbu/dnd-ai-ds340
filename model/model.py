from outlines import models
from gigax.step import NPCStepper
from huggingface_hub import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
from outlines import models
from gigax.step import NPCStepper

# Download model from the Hub
model_name = "Gigax/NPC-LLM-7B"
llm = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Our stepper takes in a Outlines model to enable guided generation
# This forces the model to follow our output format
model = models.Transformers(llm, tokenizer)

# Instantiate a stepper: handles prompting + output parsing
stepper = NPCStepper(model=model)

from gigax.parse import CharacterAction
from gigax.scene import (
    Character,
    Location,
    ProtagonistCharacter,
    ProtagonistCharacter,
    ParameterType,
)

#mabe have user fill in background information about world if neccesary if not, delete
context = "Medieval world"
current_location = Location(name="Old Town", description="A quiet and peaceful town.")
locations = [current_location] # you can add more locations to the scene

json_file_path = "npc_data.json"
with open(json_file_path, "r") as file:
    npc_data = json.load(file)

#try to import json file here
NPCs = [
    Character(
    name=npc_data.get("name"),
    description=npc_data.get("positive attributes"),
    current_location=current_location,
    )
]

new_char_file_path = "new_char.json"
with open(new_char_file_path, "r") as file:
    new_char_data = json.load(file)


#import json file here as well
protagonist = ProtagonistCharacter(
    name=new_char_data.get("name"),
    description=new_char_data.get("positive attributes"),
    current_location=current_location,
    memories=new_char_data.get("lore"),
    psychological_profile=new_char_data.get("positive attributes"),
)

action = stepper.get_action(
    context=context,
    locations=locations,
    NPCs=NPCs,
    protagonist=protagonist,
)


