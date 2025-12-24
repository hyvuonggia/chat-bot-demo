
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
    search_type="similarity",
    search_kwargs={
        "k": 30
        }
)

@tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for relevant information to answer user questions.
    
    Use this tool whenever a user asks a question that requires factual information.
    This tool searches through documents and returns relevant content.
    
    Args:
        query: The search query or question to look up in the knowledge base.
        
    Returns:
        Relevant information from the knowledge base, or a message if nothing is found.
    """
    print(f"[DEBUG RAG] search_knowledge_base called with query: {query}")
    docs = retriever.invoke(query)
    print(f"[DEBUG RAG] Retrieved {len(docs)} documents")
   
    if not docs:
         print("[DEBUG RAG] No documents found, returning empty message")
         return "No relevant documents found."

    result = "\n\n".join(f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}" for doc in docs)
    print(f"[DEBUG RAG] Returning result with {len(result)} characters")
    print(f"[DEBUG RAG] First 200 chars: {result[:200]}...")
    return result