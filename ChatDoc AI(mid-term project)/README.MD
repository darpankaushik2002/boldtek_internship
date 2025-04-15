# 📄 PDF QA Chatbot using LangChain, FAISS, Gemini & Chainlit
---------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------

![LangChain](https://img.shields.io/badge/LangChain-0.2-blue)
![Chainlit](https://img.shields.io/badge/Chainlit-Chat_UI-orange)
![Gemini](https://img.shields.io/badge/Gemini-LLM-lightgrey)
![FAISS](https://img.shields.io/badge/VectorStore-FAISS-blueviolet)



This project is an AI-powered **PDF Question Answering Chatbot** that allows users to **ask natural language questions from a PDF document**, and get answers **with context and source page links**. It uses **LangChain**, **FAISS**, **Google Gemini Pro**, and **Chainlit** to deliver a smart assistant experience.
---------------------------------------------------------------------------------------------------------

---

## 🎯 Project Aim
----------------------------------------------------------------------------------------------


The goal of this project is to build an **intelligent assistant** that:

1. 🧠 Answers user questions using content from a **specific PDF** (e.g. machine learning book).
2. 🌐 Falls back to an **internet search** if the PDF doesn't contain a confident answer.
3. 🔗 Shows **clickable source page links** from the PDF using a live viewer.
4. 📊 Uses vector similarity search to retrieve the most relevant sections.
5. 🔁 Re-ranks and verifies the answer using Gemini Pro for improved accuracy.

---

## 🧠 How It Works
----------------------------------------------------------------------------------------------

### Step-by-step logic:

1. **Vector Search from PDF (FAISS)**:
   - The PDF is split into chunks.
   - Chunks are embedded using `SentenceTransformer` (`all-mpnet-base-v2`).
   - Embeddings are stored in **FAISS**.
   - When a user asks a question, top matching chunks are retrieved.

2. **Answer Generation (Gemini Pro)**:
   - Retrieved chunks are passed to **Gemini Pro LLM** to generate an answer.

3. **Answer Evaluation Logic**:
   - It checks if the answer is **strong and grounded in the PDF** using two checks:
     - **Similarity Score**: Length of relevant chunks vs answer.
     - **LLM Rerank Prompt**: Gemini is asked if the answer is meaningful/specific based on the chunks.
   - If:
     - Similarity is high ✅ and
     - Gemini is confident ✅
     - → **Answer from PDF is shown**
   - Else → **Fallback to Internet using DuckDuckGo**

---

## 🧱 Tech Stack
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
-----------------------------------------------------------------------------------
-----------------------------------------------------------------------

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