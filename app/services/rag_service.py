
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from app.adapters.providers.openai_client import settings

# Init embedding model
embeddings = OpenAIEmbeddings(
    model=settings.openai_embed_model, 
    openai_api_key=settings.openai_api_key
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