import chainlit as cl
from dotenv import load_dotenv
import os
import shutil
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from vectordb_utils import load_faiss, save_to_faiss
from pdf_utils import process_uploaded_pdfs
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.tools import DuckDuckGoSearchRun

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Set up static serving for uploads manually if needed
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
cl.config.upload_dir = UPLOAD_DIR  # Adjusting to the newer approach

# Set up the embedding model
embedding_model = SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Hi! Please upload your PDF files to get started. (Use 📎 Attach button below)").send()

@cl.on_message
async def on_message(message: cl.Message):

    print(f"Message attributes: {dir(message)}")

    files = message.elements
    has_text = message.content.strip() != ""

    llm = cl.user_session.get("llm")
    qa_chain = cl.user_session.get("qa_chain")

    if files:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.7)
        cl.user_session.set("llm", llm)

        shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        pdf_paths = []
        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.name)
            shutil.copy(file.path, file_path)
            pdf_paths.append(file_path)

        docs = process_uploaded_pdfs(pdf_paths)
        save_to_faiss(docs)

        faiss_db = load_faiss()
        retriever = faiss_db.as_retriever(search_kwargs={"k": 3})
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

        cl.user_session.set("qa_chain", qa_chain)

        await cl.Message(content="✅ PDFs uploaded and processed successfully!").send()

        if has_text:
            await cl.Message(content=f"🤔 You asked: '{message.content}' - Now processing your question...").send()
            response = await qa_chain.acall(message.content)
            answer = response["result"]
            sources = response["source_documents"]

            top_chunks_text = [doc.page_content for doc in sources[:3]]
            length_score = sum(len(chunk.strip()) for chunk in top_chunks_text) / (len(answer.strip()) + 1)
            low_length_support = length_score < 3

            rerank_prompt = f"""You are a helpful AI assistant.
USER QUESTION: "{message.content}"
PROVIDED ANSWER: "{answer}"
Check if the answer is specific, meaningful, and grounded in the following document chunks. Just say "yes" or "no".
--- DOCUMENT CHUNKS START --- {''.join(chunk[:500] for chunk in top_chunks_text)} --- DOCUMENT CHUNKS END ---"""

            rerank_result = await llm.ainvoke(rerank_prompt)
            llm_not_confident = "no" in rerank_result.content.lower()

            if not low_length_support and not llm_not_confident:
                formatted_sources = "\n".join([
                    f"📄 {doc.metadata.get('source_file_name', 'Unknown File')} - Page {doc.metadata.get('page', 'N/A')}: {doc.page_content[:120]}..."
                    for doc in sources
                ])
                await cl.Message(content=f"💬 **Answer from PDF**:\n{answer}\n\n📚 **Sources**:\n{formatted_sources}").send()
            else:
                search = DuckDuckGoSearchRun()
                internet_result = search.run(message.content)
                await cl.Message(content=f"🌐 **Answer from Internet**:\n{internet_result}").send()

    elif has_text and qa_chain is not None: # Process subsequent text messages
        response = await qa_chain.acall(message.content)
        answer = response["result"]
        sources = response["source_documents"]

        top_chunks_text = [doc.page_content for doc in sources[:3]]
        length_score = sum(len(chunk.strip()) for chunk in top_chunks_text) / (len(answer.strip()) + 1)
        low_length_support = length_score < 3

        rerank_prompt = f"""You are a helpful AI assistant.
USER QUESTION: "{message.content}"
PROVIDED ANSWER: "{answer}"
Check if the answer is specific, meaningful, and grounded in the following document chunks. Just say "yes" or "no".
--- DOCUMENT CHUNKS START --- {''.join(chunk[:500] for chunk in top_chunks_text)} --- DOCUMENT CHUNKS END ---"""

        rerank_result = await llm.ainvoke(rerank_prompt)
        llm_not_confident = "no" in rerank_result.content.lower()

        if not low_length_support and not llm_not_confident:
            formatted_sources = "\n".join([
                f"📄 {doc.metadata.get('source_file_name', 'Unknown File')} - Page {doc.metadata.get('page', 'N/A')}: {doc.page_content[:120]}..."
                for doc in sources
            ])
            await cl.Message(content=f"💬 **Answer from PDF**:\n{answer}\n\n📚 **Sources**:\n{formatted_sources}").send()
        else:
            search = DuckDuckGoSearchRun()
            internet_result = search.run(message.content)
            await cl.Message(content=f"🌐 **Answer from Internet**:\n{internet_result}").send()

    elif has_text and qa_chain is None:
        await cl.Message(content="⚠️ No PDFs uploaded yet. Please upload first to ask questions.").send()