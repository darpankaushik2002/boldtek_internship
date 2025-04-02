import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from word2vec_embeddings import get_word2vec_embedding
from bert_embeddings import get_bert_embedding

# Function to compare cosine similarity
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Get Word2Vec embeddings
w2v_bank1 = get_word2vec_embedding("bank")
w2v_bank2 = get_word2vec_embedding("bank")

# Get BERT embeddings
b_bank1 = get_bert_embedding("The bank approved the loan.", "bank")
b_bank2 = get_bert_embedding("He sat on the river bank and fished.", "bank")

# Compute cosine similarity
w2v_similarity = cosine_similarity(w2v_bank1, w2v_bank2)
bert_similarity = cosine_similarity(b_bank1, b_bank2)

print(f"Word2Vec similarity for 'bank': {w2v_similarity:.3f}")
print(f"BERT similarity for 'bank': {bert_similarity:.3f}")

# Visualize
labels = ["Word2Vec", "BERT"]
values = [w2v_similarity, bert_similarity]

sns.barplot(x=labels, y=values)
plt.title("Similarity of 'Bank' in Different Contexts")
plt.ylabel("Cosine Similarity")
plt.show()
