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

# Load JSON data
json_file_path = "npc_data.json"
with open(json_file_path, "r") as file:
    npc_data = json.load(file)

# Extract data from JSON
name = npc_data.get("name", "Unknown NPC")
occupation = npc_data.get("occupation", "unknown occupation")
dialogue_prompt = npc_data.get("dialogue_prompt", "")

# Create the input text for the model
input_text = (
    f"NPC Profile:\n"
    f"Name: {name}\n"
    f"Occupation: {occupation}\n"
    f"Prompt: {dialogue_prompt}\n\n"
    f"NPC Response:"
)

# Tokenize and generate response
inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to("cuda")
outputs = model.generate(inputs["input_ids"], attention_mask=inputs["attention_mask"], max_length=150)

# Decode the output
npc_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Print the generated NPC dialogue or response
print("Generated NPC Response:")
print(npc_response)


