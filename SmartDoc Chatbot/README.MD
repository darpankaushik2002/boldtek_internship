📄 SmartDoc Chatbot
An AI-powered chatbot built using LangChain, Chainlit, and Google's Gemini LLM that can answer queries by retrieving information from uploaded PDF documents and the internet (DuckDuckGo).

🚀 Features
📚 Retrieve answers from uploaded PDF documents using FAISS VectorStore.

🌐 Search current events and general knowledge using DuckDuckGo Search.

💬 Chat interface powered by Chainlit for real-time interaction.

🧠 Backed by Google's Gemini LLM for high-quality responses.

🛠️ Modular tool-based agent architecture using LangChain.

🧩 Tech Stack
LangChain – For tool integration and agent-based architecture.

Chainlit – For building the interactive chat frontend.

FAISS – For storing and retrieving vector embeddings of documents.

SentenceTransformers – To embed document content (all-mpnet-base-v2).

DuckDuckGo Search API – To fetch real-time internet search results.

Gemini LLM (via Google Generative AI) – As the core language model.

📝 How It Works
Upload PDF – The PDF is converted into document chunks and embedded using SentenceTransformer.

Store in FAISS – The embeddings are saved locally in a FAISS index.

Start Chat – A Chainlit chat interface initializes with a Gemini-based LangChain agent.

Answering Queries – The agent uses:

The PDF Retriever Tool to get info from the uploaded documents.

The Internet Search Tool to fetch web-based answers via DuckDuckGo.

⚙️ Setup Instructions
Clone the repository

bash
Copy
Edit
git clone https://github.com/your-repo/smartdoc-chatbot.git
cd smartdoc-chatbot
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Set environment variables

Create a .env file with your Google API Key:

ini
Copy
Edit
GOOGLE_API_KEY=your_google_api_key_here
Run the Chainlit app

bash
Copy
Edit
chainlit run chainlit_app.py
📂 Project Structure
bash
Copy
Edit
.
├── chainlit_app.py         # Main chat app with agent initialization
├── vectordb_utils.py       # Handles FAISS save/load operations
├── requirements.txt
├── .env                    # Stores Google API key
└── README.md
✅ Example Questions
"What are the main findings of the PDF?"

"Define supervised learning."

"What is the latest news about OpenAI?"

💡 Future Improvements
Support multiple document uploads.

Enable document upload through Chainlit UI.

Integrate more advanced vector databases (like Pinecone or Chroma).