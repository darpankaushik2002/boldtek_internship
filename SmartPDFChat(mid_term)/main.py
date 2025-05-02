from pdf_utils import load_and_split_pdf
from vectordb_utils import save_to_faiss
import glob

all_docs = []
pdf_paths = glob.glob("data/*.pdf")

for pdf_path in pdf_paths:
    docs = load_and_split_pdf(pdf_path)
    for doc in docs:
        doc.metadata["source_file_name"] = pdf_path.split("/")[-1]
    all_docs.extend(docs)

save_to_faiss(all_docs)
print("✅ PDFs processed and stored in FAISS vector store.")
