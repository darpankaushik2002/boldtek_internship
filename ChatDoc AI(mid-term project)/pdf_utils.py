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

    # ✅ Offset page number metadata by +2 to match actual visual page numbers
    for doc in split_docs:
        if "page" in doc.metadata:
            doc.metadata["page"] += 1  # or 1, depending on your PDF structure

    return split_docs
