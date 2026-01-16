import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
VECTOR_STORE_DIR = "db"

def get_retriever(k_results=5):
    """
    Initializes and returns a Chroma vector store retriever.

    Args:
        k_results (int): The number of top results to retrieve.

    Returns:
        Chroma.as_retriever: A retriever object ready to find relevant documents.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    if not os.path.exists(VECTOR_STORE_DIR):
        raise FileNotFoundError(
            f"Vector store directory not found at '{VECTOR_STORE_DIR}'. "
            "Please run the `ingest.py` script first."
        )

    #embeddings = OpenAIEmbeddings(api_key=api_key)
    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
    vector_store = Chroma(
        persist_directory=VECTOR_STORE_DIR,
        embedding_function=embeddings
    )
    
    return vector_store.as_retriever(search_kwargs={"k": k_results})

if __name__ == '__main__':
    # Example usage:
    print("Testing the retriever...")
    try:
        retriever = get_retriever()
        sample_query = "How should I handle API keys?"
        results = retriever.invoke(sample_query)
        
        if results:
            print(f"\nFound {len(results)} results for query: '{sample_query}'")
            for i, doc in enumerate(results):
                print(f"\n--- Result {i+1} ---")
                print(f"Source: {doc.metadata.get('source', 'N/A')}")
                print(f"Content: {doc.page_content}")
        else:
            print("No results found.")
            
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
