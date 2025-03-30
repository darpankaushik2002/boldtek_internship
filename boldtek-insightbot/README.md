BoldTek InsightBot

Project Overview

BoldTek InsightBot is a command-line-based generative AI system that serves as a domain-specific conversational assistant. It utilizes public BoldTek documents as its knowledge base, enabling users to query information efficiently. The system integrates semantic search and generative AI to provide
context-aware responses.
-------------------------------------------------------------------------------------------------------------------------------------

Key Features:--

*Document Ingestion & Preprocessing: Extracts and splits text from multiple BoldTek sources into     meaningful overlapping chunks.

*Semantic Embeddings: Computes vector representations using a Sentence Transformer model.

*Retrieval Mechanism: Uses cosine similarity to fetch the most relevant document chunks.

*Generative AI Response: Constructs a query-specific prompt and generates responses using a pre-trained Llama-3.2-1B model via Hugging Face Transformers.

*Command-Line Interface: Provides an interactive prompt where users can enter questions.

*Virtual Environment Setup: The entire project runs within a Python virtual environment in VS Code.

*Version Control: The code is managed on GitHub to ensure a robust, version-controlled workflow.
------------------------------------------------------------------------------------------------------------------------------------


Setup Instructions

Prerequisites

Python 3.8+

VS Code (or any preferred IDE)

Virtual Environment (venv)

Hugging Face Transformers
-----------------------------------------------------------------------------------------------------------------------------------

Installation Steps

Clone the repository:



Create and activate a virtual environment:

python -m venv myvenv
source myvenv/bin/activate  # On macOS/Linux
myvenv\Scripts\activate     # On Windows

Install dependencies:

pip install -r requirements.txt

Download and place the model & tokenizer in the correct directories:

models/meta-llama/
tokenizers/meta-llama/

Run the chatbot:-

python backend/main.py
------------------------------------------------------------------------------

Future Enhancements:-

*Web-based Interface: Develop a frontend using Streamlit or Flask to replace the CLI.

*Multi-Model Support: Extend support for larger models like Llama-7B or Mistral.

*Fine-tuning on Custom Data: Train the model on specific BoldTek-related datasets for better responses.

*API Integration: Convert the system into a web API using FastAPI.

*Improved Retrieval Mechanism: Experiment with FAISS for faster and more accurate document retrieval.

*Logging & Monitoring: Implement Prometheus + Grafana for real-time system monitoring.
-------------------------------------------------------------------------------------------------------

Contact:-

For any queries, please reach out to my email - darpankaushik104@gmail.com

🚀 Developed By Darpan

