import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data/raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data/processed")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")

EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3"