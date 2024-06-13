import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os

def generate_seo_content(prompt, model_dir, temperature=0.7, top_p=0.95, top_k=50, max_length=300):
    tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
    model = GPT2LMHeadModel.from_pretrained(model_dir)

    inputs = tokenizer(prompt, return_tensors='pt')
    outputs = model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],  # Include attention mask
        max_length=max_length,  # Adjust max length to control output length
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,  # Explicitly set pad_token_id to eos_token_id
        temperature=temperature,  # Control the randomness
        top_p=top_p,  # Nucleus sampling
        top_k=top_k,  # Top-k sampling
        do_sample=True  # Enable sampling
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

if __name__ == "__main__":
    model_dir = os.path.join(os.path.dirname(__file__), "../fine_tuned_model")
    prompt = "How to optimize your website for SEO"
    seo_content = generate_seo_content(prompt, model_dir)

    print("Generated SEO Content:")
    print(seo_content)

    # Save the generated content to the results folder
    results_dir = os.path.join(os.path.dirname(__file__), "../results")
    os.makedirs(results_dir, exist_ok=True)
    with open(os.path.join(results_dir, "generated_seo_content.txt"), "w") as f:
        f.write(seo_content)
