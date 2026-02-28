📄 AI PDF Question Answering Chatbot
(RAG + FAISS + Gemini 1.5 Flash + Chainlit)

An AI-powered PDF chatbot that allows users to upload PDF documents and ask questions about their content.
The system uses Retrieval-Augmented Generation (RAG) with FAISS vector search and Gemini 1.5 Flash to provide grounded, source-backed answers.

If the model is not confident in the retrieved context, it automatically falls back to internet search (DuckDuckGo).

🚀 What This Project Does
1️⃣ Upload PDFs

User uploads one or multiple PDF files.

PDFs are:

Loaded using PyPDFLoader

Split into chunks using RecursiveCharacterTextSplitter

Embedded using all-mpnet-base-v2

Stored in a FAISS vector database

2️⃣ Ask Questions

User can ask:

“What is cloud security?”

“Explain neural networks from the book”

“What are the main threats mentioned?”

The system:

Retrieves top relevant chunks from FAISS

Sends them to Gemini (RetrievalQA)

Generates grounded answers

Shows source references (file name + page number)

3️⃣ Smart Reranking & Confidence Check

Before showing the answer:

Checks if answer is sufficiently supported by retrieved chunks

Uses LLM to validate grounding

Measures chunk-to-answer length ratio

If confidence is low →
🌐 Automatically performs DuckDuckGo search fallback

🧠 Architecture Overview

User Upload PDF
⬇
PDF Loader
⬇
Chunking (1000 size, 200 overlap)
⬇
SentenceTransformer Embeddings (all-mpnet-base-v2)
⬇
FAISS Vector Store
⬇
Retriever (Top 3 chunks)
⬇
Gemini 1.5 Flash (LLM)
⬇
Answer + Source Attribution

If low confidence → Internet Search

🛠 Tech Stack

Python

LangChain

FAISS (Vector Database)

Sentence Transformers

Google Gemini 1.5 Flash

Chainlit (Chat UI)

DuckDuckGo Search Tool

PyPDF2

python-dotenv

📂 Project Structure
├── chainlitapp.py        # Main chatbot app
├── pdf_utils.py          # PDF loading and splitting
├── vectordb_utils.py     # FAISS vector store save/load
├── main.py               # Bulk processing PDFs from /data
├── requirements.txt
├── .env                  # API keys (not committed)
├── data/
│   ├── mlbook.pdf
│   └── security_in_the_cloud.pdf
└── uploads/              # Temporary uploaded files
⚙️ Setup Instructions
1️⃣ Create Virtual Environment

Windows:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

Mac/Linux:

python -m venv .venv
source .venv/bin/activate
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Add .env file
GOOGLE_API_KEY=YOUR_API_KEY
4️⃣ Run the App
chainlit run chainlitapp.py

Then open the local URL provided.

🧪 How to Use

Click 📎 Attach button

Upload PDFs

Ask questions in chat

See:

Answer from PDF

Source file name

Page number

If answer not grounded → internet fallback

✨ Key Features

✔ Multi-PDF support
✔ Vector database retrieval
✔ LLM-powered QA
✔ Source attribution
✔ Confidence validation layer
✔ Internet fallback
✔ Clean chat UI (Chainlit)
✔ RAG architecture implementation

📈 Strenght of  this Project

This project demonstrates:

RAG (Retrieval-Augmented Generation)

Embeddings + Vector DB usage

LLM integration

Hybrid QA (documents + web)

Multi-step reasoning pipeline

Real-world AI system design

Evaluation logic (confidence scoring)

This is not just a chatbot —
This is a production-style document intelligence system.

🔮 Future Improvements

Add streaming responses

Add citation highlighting

Add document-level summarization

Add memory for conversation history

Add re-ranking with cross-encoder

Add UI confidence score indicator

Deploy on cloud (Render / Railway / HuggingFace Spaces)

👨‍💻 Author

Darpan Kaushik