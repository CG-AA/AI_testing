# transformers, torch for text generation
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json

model_id = "DevsDoCode/LLama-3-8b-Uncensored"

# load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

system_prompt = ""
user_prompt = ""

def generate_text(ai_role="assistant", max_new_tokens=512):
    try:
        with open("history.txt", "r") as file:
            chat_log = [json.loads(line) for line in file.readlines()]
    except FileNotFoundError:
        chat_log = []
    except json.JSONDecodeError:
        chat_log = []
    # initialize the message list
    messages = [{"role": "system", "content": system_prompt}] + chat_log + [{"role": "user", "content": user_prompt}]
    
    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]
    
    generated_ids = input_ids

    # open the file once before the loop
    with open("generated_output.txt", "w") as file:
        # generate tokens one by one
        for _ in range(max_new_tokens):
            outputs = model.generate(
                generated_ids,
                max_new_tokens=1,
                eos_token_id=terminators,
                do_sample=True,
                temperature=0.9,
                top_p=0.9,
            )
            next_token_id = outputs[:, -1].unsqueeze(-1)  # ensure next_token_id is 2D
            generated_ids = torch.cat((generated_ids, next_token_id), dim=-1)
            
            # decode and append the latest token to the generated text
            next_token = tokenizer.decode(next_token_id.squeeze().tolist(), skip_special_tokens=True)
            print(next_token, end="", flush=True)
            file.write(next_token)
            file.flush()
            
            if next_token_id.item() in terminators:
                break
    with open("generated_output.txt", "r") as file:
        with open("history.txt", "a") as history:
            history.write(json.dumps({"role": "user", "content": user_prompt}))
            history.write("\n")
            history.write(json.dumps({"role": ai_role, "content": file.read()}))
            history.write("\n")