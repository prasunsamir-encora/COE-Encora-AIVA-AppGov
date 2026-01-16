import os
import re
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
POLICY_FILE = "data/api_governance_policies.md"
VECTOR_STORE_DIR = "db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# --- Get API Key ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# --- 1. Load Document ---
print(f"Loading document: {POLICY_FILE}")
loader = TextLoader(POLICY_FILE)
document = loader.load()

# The document is a single large string. We need to split it by category.
doc_content = document[0].page_content

# --- 2. Split Document by Category and Create Chunks ---
print("Splitting document into chunks by category...")
# Regex to split by markdown H1 headers (# Header)
sections = re.split(r'\n# ', doc_content)
if sections[0].startswith('# '):
    sections[0] = sections[0][2:] # Clean up the very first header
else:
    sections.pop(0) # Remove any leading empty string

all_chunks = []
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,
)

for section in sections:
    if not section.strip():
        continue
    
    # The category is the first line of the section
    lines = section.split('\n')
    category_title = lines[0].strip()
    category_content = '\n'.join(lines[1:]).strip()

    # Split the content of this category into chunks
    chunks = text_splitter.split_text(category_content)
    
    # Create Document objects with metadata for each chunk
    for chunk in chunks:
        all_chunks.append(
            Document(
                page_content=chunk, 
                metadata={"category": category_title, "source": POLICY_FILE}
            )
        )

print(f"Created {len(all_chunks)} chunks from {len(sections)} categories.")

# --- 3. Create Embeddings and Store in ChromaDB ---
# Before creating new embeddings, let's clear the old vector store directory
if os.path.exists(VECTOR_STORE_DIR):
    import shutil
    print(f"Removing old vector store directory: {VECTOR_STORE_DIR}")
    shutil.rmtree(VECTOR_STORE_DIR)

print("Creating embeddings and storing in ChromaDB...")
#embeddings = OpenAIEmbeddings(model="text-embedding-3-large",api_key=api_key)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
# Create a new Chroma DB from the prepared chunks
vector_store = Chroma.from_documents(
    documents=all_chunks,
    embedding=embeddings,
    persist_directory=VECTOR_STORE_DIR
)

print(f"Successfully ingested data and saved vector store to: {VECTOR_STORE_DIR}")
print("--- Ingestion Complete ---")