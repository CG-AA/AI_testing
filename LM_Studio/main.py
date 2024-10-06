from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load the tokenizer and model
model_id = "gpt2"  # Replace with your model ID
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id).to("cuda")

def generate_text(prompt, max_new_tokens=50, batch_size=4):
    # Tokenize the input prompt
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
    
    # Repeat input_ids to match the batch size
    input_ids = input_ids.repeat(batch_size, 1)
    
    # Generate text
    outputs = model.generate(
        input_ids,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
    )
    
    # Decode the generated text
    generated_texts = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    
    return generated_texts

# Example usage
prompt = "Once upon a time"
generated_texts = generate_text(prompt, max_new_tokens=50, batch_size=4)
for i, text in enumerate(generated_texts):
    print(f"Generated Text {i+1}:\n{text}\n")