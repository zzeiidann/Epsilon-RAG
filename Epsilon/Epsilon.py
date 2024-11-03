import pdfplumber
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Replace with your PDF file path
pdf_file = "/Users/mraffyzeidan/Documents/Code/Epsilon/data/Project Modsur.pdf"
text_from_pdf = extract_text_from_pdf(pdf_file)
print("Text extracted from PDF:")
print(text_from_pdf[:500])  # Print first 500 characters as example

# Tokenization using GPT-2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Tokenize the text
inputs = tokenizer(text_from_pdf, return_tensors="pt", truncation=True, max_length=1024)

# Prepare train dataset
train_dataset = inputs

# Configuration and training arguments
model = GPT2LMHeadModel.from_pretrained("gpt2")
training_args = TrainingArguments(
    output_dir="./results",  # Replace with desired output directory
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=500,  # Number of updates steps before saving checkpoint
    logging_dir='./logs',
    logging_steps=100,  # Number of steps before logging updates
    evaluation_strategy="epoch",  # Evaluation strategy during training
)

# Trainer for training the model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

# Start training
trainer.train()
