
from langchain_community.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from app.adapters.providers.openai_client import settings

# Init embedding model
embeddings = OpenAIEmbeddings(
    model=settings.openai_embed_model, 
)

# Init vector store (Chroma)
vector_store = Chroma(
    persist_directory=settings.chroma_db_path,
    embedding_function=embeddings,
    collection_name="chatbot_knowledge"
)

retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k": 5,
        "score_threshold": 0.5
        }
)

@tool
def search_knowledge_base(query: str) -> str:
    """Function to search knowledge base using the retriever."""
    docs = retriever.invoke(query)
   
    if not docs:
         return "No relevant documents found."

    return "\n\n".join(f"[Source: {doc.metadata.get("source", "Unknown")}]" for doc in docs)