import glob

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core import documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import embeddings

from app.services.rag_service import settings


def ingest_documents():
    print("--- 1. INGESTING DOCUMENTS FROM KNOWLEDGE BASE... ---")
    folder_path = "knowledge_base"
    
    all_files = glob.glob(f"{folder_path}/**/*.txt", recursive=True)
    
    if not all_files:
        print("No text files found in the knowledge_base folder.")
        return
    
    documents = []
    for file_path in all_files:
        try:
            print(f"Reading file: {file_path}")
            
            # load text file
            loader = TextLoader(file_path, encoding="utf-8")  
            docs = loader.load()
            
            # add metadata
            for doc in docs:
                doc.metadata["source"] = file_path
                
            documents.extend(docs)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            
    print("--- 2. SPLITTING DOCUMENTS INTO CHUNKS... ---")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    
    print("--- 3. SAVING CHUNKS TO VECTOR STORE... ---")
    embeddings_model = embeddings.OpenAIEmbeddings(
        model=settings.openai_embed_model,
    )
    
    # Init vector store (Chroma)
    vector_store = Chroma(
        persist_directory=settings.chroma_db_path,
        embedding_function=embeddings_model,
        collection_name="chatbot_knowledge"
    )
    
    if chunks:
        vector_store.add_documents(chunks)
        print("Ingestion completed successfully.")
    else:
        print("No chunks to add to the vector store.")
        
        
if __name__ == "__main__":
    ingest_documents()
        
        
    