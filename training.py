""" 
This scrip will generate a new model based on the trainning_dataset.csv and save it in the models folder.

 """

import pandas as pd
from datasets import Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Load model and tokenizer
model_name = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
#tokenizer = AutoTokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
#model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Training Data

def load_data(file_path):
    df = pd.read_csv(file_path)
    return Dataset.from_pandas(df)

# Tokenization function
def preprocess_function(examples):
    inputs = examples["input"]
    targets = examples["output"]
    model_inputs = tokenizer(inputs, max_length=128, padding="max_length", truncation=True)

    # Tokenize the targets with the `labels` key
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=128, padding="max_length", truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Load dataset
data_path = "trainning_dataset.csv"
dataset = load_data(data_path)

# Tokenize inputs and outputs
inputs = tokenizer([d["input"] for d in dataset], return_tensors="pt",  truncation=True, max_length=128, padding="max_length")
outputs = tokenizer([d["output"] for d in dataset], return_tensors="pt",  truncation=True, max_length=128, padding="max_length")

labels = outputs["input_ids"]
labels[labels == tokenizer.pad_token_id] = -100  # Ignore padding in the loss calculation

# Define optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

# Training loop
model.train()
for epoch in range(60):  # 60 epochs
    optimizer.zero_grad()
    outputs = model(input_ids= inputs["input_ids"], attention_mask=inputs["attention_mask"], labels=labels)
    loss = outputs.loss
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch + 1}, Loss: {loss.item()}")

# Save the model
model.save_pretrained("./robot_instruction_model")
tokenizer.save_pretrained("./robot_instruction_model")
