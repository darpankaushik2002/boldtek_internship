# backend/data_analysis.py
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load a pre-trained sentence transformer for embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def load_documents(data_dir: str):
    """
    Load all text documents from the specified directory.
    Returns a list of tuples: (filename, content).
    """
    documents = []
    for file in Path(data_dir).glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            documents.append((file.name, content))
    return documents

def chunk_text(text: str, chunk_size: int = 40, overlap: int = 10):
    """
    Split text into chunks of 'chunk_size' words with an overlap of 'overlap' words.
    Using 20-word chunks should produce more concise and focused context pieces.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

def build_index(data_dir: str):
    """
    Load documents from the data directory, split them into smaller chunks,
    compute embeddings for each chunk, and return a list of (chunk_text, embedding) tuples.
    """
    index = []
    documents = load_documents(data_dir)
    for filename, content in documents:
        chunks = chunk_text(content)
        for chunk in chunks:
            emb = embedding_model.encode(chunk)
            index.append((chunk, emb))
    return index

def retrieve_relevant_chunks(query: str, index, top_k: int = 3):
    """
    Given a query, compute its embedding and retrieve the top_k most similar text chunks.
    Returns a list of tuples: (chunk_text, similarity_score).
    """
    query_emb = embedding_model.encode(query)
    similarities = [(chunk, cosine_similarity([query_emb], [emb])[0][0]) for chunk, emb in index]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]
