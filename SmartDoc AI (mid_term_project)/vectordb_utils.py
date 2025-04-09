from langchain_community.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
import os
import pickle

sentence_transformer_ef = SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")


FAISS_INDEX_FILE = "faiss_index"

def save_to_faiss(docs):
    db = FAISS.from_documents(docs, sentence_transformer_ef)
    db.save_local(FAISS_INDEX_FILE)

def load_faiss():
    return FAISS.load_local(FAISS_INDEX_FILE, sentence_transformer_ef, allow_dangerous_deserialization=True)

