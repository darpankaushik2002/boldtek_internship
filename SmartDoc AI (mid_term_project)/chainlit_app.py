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

@cl.on_chat_start
async def on_chat_start():
    # Initialize Gemini LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.8)

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

    response = qa_chain(message.content)
    answer = response["result"]
    sources = response["source_documents"]

    # Define fallback triggers (phrases that signal PDF has no useful info)
    fallback_phrases = [
        "not in the document", "not mentioned", "does not contain", "not covered",
        "outside the scope", "no relevant information", "irrelevant", "i don't know",
        "unable to", "sorry", "can't find", "no information","provides information on",
    ]

    should_fallback = (
        not answer or
        len(answer.strip()) < 15 or
        any(phrase in answer.lower() for phrase in fallback_phrases)
    )

    if not should_fallback:
        # Show PDF answer and sources
        formatted_sources = "\n".join([
            f"📄 Page {doc.metadata.get('page', 'N/A')}: {doc.page_content[:100]}..."
            for doc in sources
        ])
        await cl.Message(
            content=f"💬 **Answer from PDF**:\n{answer}\n\n📚 **Sources**:\n{formatted_sources}"
        ).send()
    else:
        # Fallback to DuckDuckGo internet search
        search = DuckDuckGoSearchRun()
        internet_result = search.run(message.content)

        await cl.Message(
            content=f"🌐 **Answer from Internet**:\n{internet_result}"
        ).send()
