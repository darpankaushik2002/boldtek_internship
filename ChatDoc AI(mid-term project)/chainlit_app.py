import os
import chainlit as cl
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import DuckDuckGoSearchRun
from vectordb_utils import load_faiss

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Function to generate a link to a specific PDF page using PDF.js viewer
def generate_pdf_link(page_num):
    raw_pdf_url = "https://raw.githubusercontent.com/darpankaushik2002/DAP-PROGRAMS/main/ml_book.pdf"
    return f"https://mozilla.github.io/pdf.js/web/viewer.html?file={raw_pdf_url}#page={page_num}"

@cl.on_chat_start
async def on_chat_start():
    # Initialize Gemini LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.8)

    # Load FAISS vector store
    faiss_db = load_faiss()
    retriever = faiss_db.as_retriever(search_kwargs={"k": 3})

    # Wrap retriever with QA chain
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

    # Save tools and LLM to session
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

    # Step 2: Cosine similarity check (manual threshold)
    top_chunks_text = [doc.page_content for doc in sources[:3]]
    similarity_score = sum(len(chunk.strip()) for chunk in top_chunks_text) / (len(answer.strip()) + 1)
    low_similarity = similarity_score < 3  # Tune threshold if needed

    # Step 3: Reranking with LLM to verify answer quality
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

    # Step 4: Decision logic
    if not low_similarity and not llm_not_confident:
        # Show answer from PDF with clickable links
        formatted_sources = "\n".join([
            f"📄 [Page {doc.metadata.get('page', 'N/A')}]({generate_pdf_link(doc.metadata.get('page', 1))}): {doc.page_content[:120]}..."
            for doc in sources
        ])
        await cl.Message(
            content=f"💬 **Answer from PDF**:\n{answer}\n\n📚 **Sources**:\n{formatted_sources}"
        ).send()
    else:
        # Fallback to internet
        search = DuckDuckGoSearchRun()
        internet_result = search.run(message.content)

        await cl.Message(
            content=f"🌐 **Answer from Internet**:\n{internet_result}"
        ).send()
