import torch
from transformers import BertTokenizer, BertModel

# Load dataset
with open("data/corpus.txt", "r") as f:
    documents = f.readlines()

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert_model = BertModel.from_pretrained("bert-base-uncased")

def get_bert_embedding(sentence, target_word):
    tokens = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)
    
    with torch.no_grad():
        outputs = bert_model(**tokens)
    
    # Extract contextual embedding for the target word
    tokenized_input = tokenizer.tokenize(sentence)
    word_index = tokenized_input.index(target_word) if target_word in tokenized_input else 0
    word_embedding = outputs.last_hidden_state[:, word_index, :].squeeze().numpy()
    
    return word_embedding

# Example: Compare embeddings of "bank" in different sentences
bank1_embedding = get_bert_embedding("The bank approved the loan.", "bank")
bank2_embedding = get_bert_embedding("He sat on the river bank and fished.", "bank")

print("BERT - Bank (Finance):", bank1_embedding[:5])
print("BERT - Bank (River):", bank2_embedding[:5])
