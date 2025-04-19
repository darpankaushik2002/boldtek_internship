import os
import chainlit as cl
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.embeddings import SentenceTransformerEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from vectordb_utils import load_faiss

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Embedding model for semantic similarity
embedding_model = SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")

# PDF link generator
def generate_pdf_link(page_num):
    raw_pdf_url = "https://raw.githubusercontent.com/darpankaushik2002/DAP-PROGRAMS/main/ml_book.pdf"
    return f"https://mozilla.github.io/pdf.js/web/viewer.html?file={raw_pdf_url}#page={page_num}"

@cl.on_chat_start
async def on_chat_start():
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.8)
    faiss_db = load_faiss()
    retriever = faiss_db.as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

    cl.user_session.set("qa_chain", qa_chain)
    cl.user_session.set("llm", llm)

    await cl.Message(content="Hi 👋! Ask me anything — I’ll first search your PDF and then the internet if needed.").send()

@cl.on_message
async def on_message(message: cl.Message):
    qa_chain = cl.user_session.get("qa_chain")
    llm = cl.user_session.get("llm")

    # Step 1: Get answer and top documents from FAISS PDF search
    response = qa_chain(message.content)
    answer = response["result"]
    sources = response["source_documents"]
    top_chunks_text = [doc.page_content for doc in sources[:3]]
    """
    Didn't Use Cosine Similarity because:-
     already used FAISS, which does cosine similarity behind the scenes when retrieving PDF chunks.

     length heuristic + reranker LLM are faster and easier to interpret.

    Cosine similarity between query and chunk doesn’t always mean the answer is   well-supported — my method checks support, not just similarity.


    # Step 2a: Cosine similarity (semantic)
    #query_embedding = embedding_model.embed_query(message.content)
    #combined_text = " ".join(top_chunks_text)
    retrieved_embedding = embedding_model.embed_query(combined_text)
    cosine_sim_score = cosine_similarity([query_embedding], [retrieved_embedding])[0][0]
    low_cosine_sim = cosine_sim_score < 0.5
    """
    # Step 2b: Length heuristic (structure-based)
    length_score = sum(len(chunk.strip()) for chunk in top_chunks_text) / (len(answer.strip()) + 1)
    low_length_support = length_score < 3
    """
    sum(len(chunk.strip()) for chunk in top_chunks_text) → This is the total number of characters in the top 3 chunks retrieved from the PDF.

    len(answer.strip()) + 1 → This is the length of the answer, with +1 to avoid division by zero.

    ✅ High Score (≥ 3):
    Means the retrieved chunks contain a good amount of text compared to the answer.

    Suggests that the LLM likely used the PDF content to generate the response.

    ⚠️ Low Score (< 3):
    Means the PDF content might be too short or unrelated compared to the answer length.

    Suggests the LLM might be hallucinating or guessing without enough support.
    
    """

    # Step 3: Reranking with LLM
    rerank_prompt = f"""
You are a helpful AI assistant.

USER QUESTION: "{message.content}"  
PROVIDED ANSWER: "{answer}"  


Check if the answer is specific, meaningful, and grounded in the following text chunks from the document. 
Just say "yes" or "no".

--- DOCUMENT CHUNKS START ---
{''.join(chunk[:500] for chunk in top_chunks_text)}
--- DOCUMENT CHUNKS END ---
"""
    rerank_result = llm.invoke(rerank_prompt)
    llm_not_confident = "no" in rerank_result.content.lower()

    # Step 4: Hybrid Decision Logic
    if  not low_length_support and not llm_not_confident:
        # Show PDF answer with source links
        formatted_sources = "\n".join([
            f"📄 [Page {doc.metadata.get('page', 'N/A')}]({generate_pdf_link(doc.metadata.get('page', 1))}): {doc.page_content[:120]}..."
            for doc in sources
        ])
        await cl.Message(
            content=f"💬 **Answer from PDF**:\n{answer}\n\n📚 **Sources**:\n{formatted_sources}"
        ).send()
    else:
        # Fallback to DuckDuckGo
        search = DuckDuckGoSearchRun()
        internet_result = search.run(message.content)
        await cl.Message(
            content=f"🌐 **Answer from Internet**:\n{internet_result}"
        ).send()
