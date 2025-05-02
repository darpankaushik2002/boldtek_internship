from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_split_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    split_docs = text_splitter.split_documents(pages)

    for doc in split_docs:
        if "page" in doc.metadata:
            doc.metadata["page"] += 1  # Because PyPDFLoader is 0-indexed
    return split_docs

def process_uploaded_pdfs(pdf_paths):
    all_docs = []
    for path in pdf_paths:
        docs = load_and_split_pdf(path)
        for doc in docs:
            doc.metadata["source_file_name"] = path.split("/")[-1]
        all_docs.extend(docs)
    return all_docs
