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

#try to import json file here
NPCs = [
    Character(
    name="John the Brave",
    description="A fearless warrior",
    current_location=current_location,
    )
]

#import json file here as well
protagonist = ProtagonistCharacter(
    name="Aldren",
    description="Brave and curious",
    current_location=current_location,
    memories=["Saved the village", "Lost a friend"],
    quests=["Find the ancient artifact", "Defeat the evil warlock"],
    skills=[
        Skill(
            name="Attack",
            description="Deliver a powerful blow",
            parameter_types=[ParameterType.character],
        )
    ],
    psychological_profile="Determined and compassionate",
)

action = stepper.get_action(
    context=context,
    locations=locations,
    NPCs=NPCs,
    protagonist=protagonist,
)


