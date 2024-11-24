from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from torch.utils.data import Dataset
import pandas as pd
from datasets import Dataset as pdDataset
import torch

# Tokenizer and model
model_name = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


# Training Data

def load_data(file_path):
    df = pd.read_csv(file_path)
    return pdDataset.from_pandas(df)



def preprocess_function(train_data):
    train_encodings = tokenizer(
        [item["input"] for item in train_data],
        truncation=True,
        padding=True,
        max_length=128,
        return_tensors="pt",
    )
    train_labels = tokenizer(
        [item["output"] for item in train_data],
        truncation=True,
        padding=True,
        max_length=128,
        return_tensors="pt",
    ).input_ids
    return train_encodings, train_labels


class T5Dataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.encodings["input_ids"])

    def __getitem__(self, idx):
        return {
            "input_ids": self.encodings["input_ids"][idx],
            "attention_mask": self.encodings["attention_mask"][idx],
            "labels": self.labels[idx],
        }


# Load dataset
data_path = "trainning_dataset.csv"
train_data = load_data(data_path)

# Evaluation data
eval_path = "evaluation_dataset.csv"
eval_data = load_data(eval_path)

train_encodings, train_labels = preprocess_function(train_data)
eval_encodings, eval_labels = preprocess_function(eval_data)


# Create datasets
train_dataset = T5Dataset(train_encodings, train_labels)
eval_dataset = T5Dataset(eval_encodings, eval_labels)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="steps",
    eval_steps=10,
    save_steps=50,
    logging_dir="./logs",
    logging_steps=50,
    per_device_train_batch_size=4,
    num_train_epochs=50,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,  # Add evaluation dataset
)

optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
trainer.optimizer = optimizer

# Train
trainer.train()

# Save the model
model.save_pretrained("./robot_instruction_model")
tokenizer.save_pretrained("./robot_instruction_model")
