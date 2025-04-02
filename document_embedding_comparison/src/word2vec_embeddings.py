import nltk
import numpy as np
from gensim.models import Word2Vec

nltk.download('punkt')

# Load dataset
with open("data/corpus.txt", "r") as f:
    documents = f.readlines()

# Tokenize sentences
tokenized_docs = [nltk.word_tokenize(doc.lower()) for doc in documents]

# Train Word2Vec model
word2vec_model = Word2Vec(sentences=tokenized_docs, vector_size=100, window=5, min_count=1, workers=4)

def get_word2vec_embedding(word):
    if word in word2vec_model.wv:
        return word2vec_model.wv[word]
    else:
        return np.zeros(word2vec_model.vector_size)

# Example: Compare embeddings of "bank" and "bat"
bank_embedding = get_word2vec_embedding("bank")
bat_embedding = get_word2vec_embedding("bat")

print("Word2Vec - Bank:", bank_embedding[:5])  # Show first 5 values
print("Word2Vec - Bat:", bat_embedding[:5])
