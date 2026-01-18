import os
import sys
from dotenv import load_dotenv

# 1. FORCE LOAD ENV
load_dotenv()

# 2. CHECK KEY
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("CRITICAL ERROR: OPENAI_API_KEY not found.")
    sys.exit(1)

from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Configuration
PERSIST_DIRECTORY = "./chroma_db"
EMBEDDING_MODEL = OpenAIEmbeddings(model="text-embedding-3-small")

def index_codebase(root_path: str):
    print(f"🔍 Starting scan of: {root_path}")

    # --- SDE 3: SAFE LOADING ---
    # Only load files, but we will filter them manually to be safe
    loader = GenericLoader.from_filesystem(
        root_path,
        glob="**/*",
        suffixes=[".py"], 
        parser=LanguageParser(language=Language.PYTHON, parser_threshold=500)
    )
    all_documents = loader.load()
    
    # FILTER: Remove 'venv', '.git', 'site-packages', and '__pycache__'
    documents = []
    for doc in all_documents:
        source = doc.metadata.get("source", "")
        if "venv" in source or "site-packages" in source or "__pycache__" in source or ".git" in source:
            continue
        documents.append(doc)

    print(f"📄 Found {len(documents)} Clean Python files (filtered out venv/libraries).")

    if not documents:
        return {"status": "error", "message": "No valid Python files found. Check your path!"}

    # Split Code
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, 
        chunk_size=1000, 
        chunk_overlap=100
    )
    texts = splitter.split_documents(documents)
    print(f"✂️  Split code into {len(texts)} chunks.")
    
    if not texts:
         return {"status": "error", "message": "Code found but chunks are empty."}

    # Save to Database
    print(f"💾 Sending {len(texts)} chunks to OpenAI Embeddings...")
    try:
        db = Chroma.from_documents(
            documents=texts, 
            embedding=EMBEDDING_MODEL, 
            persist_directory=PERSIST_DIRECTORY
        )
    except Exception as e:
        print(f"❌ OpenAI Error: {e}")
        return {"status": "error", "message": str(e)}
    
    return {"status": "success", "chunks_indexed": len(texts)}

def get_retriever():
    db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=EMBEDDING_MODEL)
    return db.as_retriever(search_kwargs={"k": 5})