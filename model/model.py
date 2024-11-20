from outlines import models
from gigax.step import NPCStepper
from huggingface_hub import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model and tokenizer
model_name_or_path = "npc_llm_7b"
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, device_map="auto", torch_dtype="auto")

# Set a distinct padding token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Prepare input
input_text = "Hello, how can I assist you?"
inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to("cuda")

# Pass attention mask explicitly
outputs = model.generate(
    inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    max_length=50
)

# Decode output
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

