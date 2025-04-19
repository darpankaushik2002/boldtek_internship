# 📚 PDF Q&A Assistant using LangChain, FAISS, and Gemini LLM

A smart conversational assistant that allows users to query PDF documents with natural language. It uses **LangChain**, **FAISS**, and **Gemini (Google Generative AI)** to retrieve and generate precise answers from PDF content. If the document lacks enough information, it intelligently falls back to the internet for a reliable answer.

---

## 🎯 Project Aim
--------------------------------------------------------------------------------------

To build an intelligent chatbot that:
- Understands and answers questions based on the content of a given PDF (e.g., books, manuals, reports).
- Ensures the answers are grounded in document content using semantic search, heuristic checks, and LLM reranking.
- Provides internet-sourced fallback answers when the document information is insufficient.

---

## 🚀 Features
------------------------------------------------------------------------------------------------

✅ **PDF Ingestion**  
- Loads and splits PDF into meaningful chunks using LangChain's `PyPDFLoader` and `RecursiveCharacterTextSplitter`.

✅ **Semantic Vector Search**  
- Embeds document chunks using `all-mpnet-base-v2` Sentence Transformer.
- Stores and retrieves chunks using FAISS for fast, similarity-based searching.

✅ **Q&A with Gemini LLM**  
- Uses `Gemini 1.5 Flash` for generating responses.
- Queries PDF via a `RetrievalQA` chain with LangChain.

✅ **Confidence Scoring**  
- Uses a length-based heuristic to check if the answer is well-supported by the PDF content.
- Reranks answers using an LLM prompt to validate answer quality.

✅ **Fallback to Internet Search**  
- Uses DuckDuckGo search when the PDF content isn't sufficient or reliable.

✅ **Chainlit Frontend**  
- Engaging conversational UI powered by Chainlit.
- Shows source snippets with clickable page links from the original PDF.

---

## 🛠️ How It Works
------------------------------------------------------------------------------------------------

1. **PDF Preprocessing (`main.py`)**
   - The PDF is loaded and split into chunks using LangChain’s `PyPDFLoader` and `RecursiveCharacterTextSplitter`.
   - Each chunk is embedded using a Sentence Transformer model (`all-mpnet-base-v2`).
   - The chunks and their embeddings are stored in a FAISS vector store for efficient similarity search.

2. **Chat Session Starts (`chainlitapp.py`)**
   - Chainlit launches a conversational UI.
   - The Gemini LLM and FAISS retriever are initialized.
   - A friendly welcome message invites the user to ask questions.

3. **Question Handling**
   - The user submits a question.
   - LangChain’s `RetrievalQA` retrieves relevant chunks from the FAISS store.
   - Gemini LLM generates an answer based on those chunks.

4. **Confidence Checks**
   - **Heuristic Check**: Measures how well the length of the PDF chunks supports the generated answer.
   - **LLM Reranking**: The Gemini LLM is asked to evaluate if the answer is grounded in the retrieved chunks.

5. **Hybrid Decision Logic**
   - If both checks pass: ✅ The answer is shown along with source links to the PDF pages.
   - If not: ❌ The system uses DuckDuckGo to search the web and returns an internet-based answer instead.

6. **PDF Source Links**
   - The app generates page-specific links using `pdf.js`, so users can directly view the original content.

---

## 🧠 Architecture Overview
----------------------------------------------------------------------------------------------------

```text
                ┌────────────────────┐
                │   PDF Document     │
                └────────┬───────────┘
                         ▼
              ┌─────────────────────┐
              │  load_and_split_pdf │ ←─ PyPDFLoader + RecursiveCharacterTextSplitter
              └────────┬────────────┘
                       ▼
              ┌─────────────────────┐
              │   FAISS Vector DB   │ ←─ SentenceTransformerEmbeddings
              └────────┬────────────┘
                       ▼
       ┌─────────────────────────────────┐
       │      RetrievalQA + Gemini LLM   │
       └────────┬────────────────────────┘
                ▼
   ┌─────────────────────────────────────────┐
   │   Length Heuristic + LLM Reranking      │
   └────┬────────────────────────────────────┘
        ▼
┌─────────────┐       No        ┌────────────────────────┐
│  PDF Answer │◄───────────────┤   Internet Fallback     │
└─────────────┘                └────────────────────────┘




---

## 🧱 Tech Stack
------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------

| Component            | Description                                    |
|----------------------|------------------------------------------------|
| `LangChain`          | Chain logic + retrieval QA                    |
| `FAISS`              | Vector store for chunk embeddings              |
| `SentenceTransformer`| Embedding model (`all-mpnet-base-v2`)          |
| `Gemini Pro`         | LLM from Google Generative AI                  |
| `DuckDuckGo Tools`   | Internet search fallback                       |
| `Chainlit`           | Chat-based frontend for LLM apps               |
| `PyPDFLoader`        | For loading and splitting PDFs                 |

---

## ⚙️ Setup Instructions
----------------------------------------------------------------------



```bash
git clone https://github.com/your-repo/smartdoc-chatbot.git
cd smartdoc-chatbot
pip install -r requirements.txt
Create a .env file:

GOOGLE_API_KEY=your_google_api_key_here
Run preprocessing:-
python main.py
Start chatbot:-
chainlit run chainlit_app.py --port 8000

📁 Folder Structure
-----------------------------------------------------
.
├── main.py                # Preprocess and index PDF
├── chainlit_app.py        # Chat app and agent logic
├── pdf_utils.py           # PDF loading and chunking
├── vectordb_utils.py      # FAISS DB operations
├── data/ml_book.pdf       # PDF file
├── .env                   # API key
├── requirements.txt
└── README.md


✅ Example Prompts
-----------------------------------------------------------------
"what is NLP"

"What is YOLO ?"

"What is GPT model Architecture?"

💡 Future Enhancements
-------------------------------------------------------------------------
Allow PDF upload via Chainlit UI

Multi-document support

Add LangGraph-based agent flow

Integration with advanced vector DBs like Pinecone, Weaviate

Built with ❤️ by Darpan using LangChain, Chainlit, and Gemini