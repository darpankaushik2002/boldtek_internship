📄 Chainlit PDF Chatbot with Gemini 1.5 Flash, FAISS & DuckDuckGo Fallback
An interactive PDF question-answering chatbot powered by Gemini 1.5 Flash, LangChain, FAISS, and Chainlit. Users can upload PDFs, ask questions, and receive context-aware answers grounded in document content — with intelligent reranking and fallback to DuckDuckGo if confidence is low.

🚀 Features
📎 Upload PDFs via Chainlit UI

🧠 Answer questions using Gemini 1.5 Flash

📚 Retrieve relevant chunks from PDFs with FAISS

✅ Rerank answers for grounding and quality

🌐 Fallback to DuckDuckGo if PDF-based answer is weak

💾 Persistent FAISS vector index

🧩 Built with LangChain, SentenceTransformer, and Chainlit

🧱 Project Structure

📁 your_project/
│
├── chainlitapp.py           # Main Chainlit app logic
├── main.py                  # Pre-index PDFs from `data/` into FAISS
├── pdf_utils.py             # PDF loading and chunking logic
├── vectordb_utils.py        # FAISS save/load helpers
├── data/                    # Folder for pre-indexed PDFs
├── uploads/                 # Runtime upload storage
├── .env                     # API keys (e.g., GOOGLE_API_KEY)
└── requirements.txt         # Required Python packages

💡 How It Works
User uploads PDF(s) via Chainlit interface.

PDFs are processed and split into chunks using RecursiveCharacterTextSplitter.

Chunks are embedded using all-mpnet-base-v2 and saved in FAISS.

A RetrievalQA chain is created with Gemini 1.5 Flash.

User's query is answered based on top-k document chunks.

A reranking prompt checks if the answer is grounded in context:

✅ If confident → show answer with sources.

❌ If low confidence → fall back to DuckDuckGo search.

📦 Dependencies
Example requirements.txt:


langchain
langchain-community
langchain-google-genai
chainlit
sentence-transformers
duckduckgo-search
python-dotenv
PyMuPDF



🧠 Model & Tools
LLM: gemini-1.5-flash-latest

Embeddings: all-mpnet-base-v2 (SentenceTransformers)

Retriever: FAISS vector DB

Search fallback: DuckDuckGo via DuckDuckGoSearchRun

Interface: Chainlit

✅ Example Usage
Upload a PDF (e.g., "product_manual.pdf").

Ask a question like:
"What are the safety instructions mentioned?"

Get an accurate answer from the document, or fallback to web if needed.

📌 Notes
PDFs uploaded during runtime are stored temporarily in uploads/.

FAISS index is saved locally (faiss_index/).

Supports reranking for trustworthy, grounded answers.





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

📬 Contact
Made with ❤️ by Darpan.
Feel free to reach out for questions, suggestions, or collaboration.