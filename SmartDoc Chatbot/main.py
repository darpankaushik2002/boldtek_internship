from pdf_utils import load_and_split_pdf
from vectordb_utils import save_to_faiss

pdf_path = "data/ml_book.pdf"
docs = load_and_split_pdf(pdf_path)
save_to_faiss(docs)
print("✅ PDF processed and stored in FAISS vector store.")
