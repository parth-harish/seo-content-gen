from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
import torch
from torch.utils.data import Dataset
import os

class MyTextDataset(Dataset):
    def __init__(self, tokenizer, file_path, block_size=512):
        self.examples = []

        with open(file_path, encoding="latin-1") as f:  # Use latin-1 encoding to handle a wider range of characters
            text = f.read()

        tokenized_text = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(text))

        for i in range(0, len(tokenized_text) - block_size + 1, block_size):
            self.examples.append(
                torch.tensor(tokenized_text[i:i + block_size], dtype=torch.long)
            )

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, item):
        return self.examples[item]

def load_dataset(file_path, tokenizer):
    return MyTextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=128,
    )

def fine_tune_model(train_file):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    train_dataset = load_dataset(train_file, tokenizer)
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    training_args = TrainingArguments(
        output_dir=os.path.join(os.path.dirname(train_file), "../results"),
        overwrite_output_dir=True,
        num_train_epochs=3,  # Increase the number of epochs
        per_device_train_batch_size=1,
        save_steps=10_000,
        save_total_limit=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
    )

    trainer.train()
    model.save_pretrained(os.path.join(os.path.dirname(train_file), "../fine_tuned_model"))
    tokenizer.save_pretrained(os.path.join(os.path.dirname(train_file), "../fine_tuned_model"))

if __name__ == "__main__":
    train_file = os.path.join(os.path.dirname(__file__), "../data/preprocessed_articles.txt")
    fine_tune_model(train_file)
