import os
import chainlit as cl
from langchain.chains import RetrievalQA
from langchain.agents import Tool, initialize_agent
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from vectordb_utils import load_faiss

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

@cl.on_chat_start
async def on_chat_start():
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.8)

    # Load FAISS vector store and retriever
    faiss_db = load_faiss()
    retriever = faiss_db.as_retriever(search_kwargs={"k": 3})

    # Wrap retriever with RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Define tools
    tools = [
        Tool(
            name="Internet Search",
            func=DuckDuckGoSearchRun().run,
            description="Useful for answering questions about current events or things not in the documents."
        ),
        Tool(
            name="PDF Retriever",
            func=qa_chain.run,
            description="Useful for answering questions from the uploaded documents."
        ),
    ]

    # Initialize agent with tools
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    # Save agent and retriever to session
    cl.user_session.set("agent", agent)

    # Optional: welcome message
    await cl.Message(content="Hi 👋! Ask me anything — I’ll search your PDF and the internet as needed.").send()

@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")

    try:
        # Run agent with user's message
        response = await cl.make_async(agent.run)(message.content)

        # Send response back
        await cl.Message(content=response).send()

    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()
