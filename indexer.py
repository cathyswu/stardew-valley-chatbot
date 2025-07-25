import os
from bs4 import BeautifulSoup
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from config import RAW_DIR, CHROMA_DB_DIR, EMBEDDING_MODEL

def clean_html_content(html_content):
    """Clean HTML content for better RAG processing"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted elements
    for element in soup.select('nav, .navbox, .toc, script, style, .mw-editsection, .printfooter'):
        element.decompose()
    
    # Remove navigation menus and footers
    for element in soup.select('.navigation-not-searchable, .mw-footer, .mw-navigation'):
        element.decompose()
    
    # Focus on main content
    main_content = soup.select_one('#mw-content-text')
    if main_content:
        return main_content.get_text(separator='\n', strip=True)
    else:
        return soup.get_text(separator='\n', strip=True)

def load_docs():
    docs = []
    files = [f for f in os.listdir(RAW_DIR) if f.endswith(".html")]
    print(f"Found {len(files)} HTML files to index...")
    for i, fname in enumerate(files, 1):
        path = os.path.join(RAW_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            html_content = f.read()
            clean_content = clean_html_content(html_content)
            if clean_content and len(clean_content.strip()) > 100:  # Only add substantial content
                docs.append(Document(page_content=clean_content, metadata={"source": fname}))
        if i % 10 == 0 or i == len(files):
            print(f"Processed {i}/{len(files)} files")

    print(f"Loaded {len(docs)} documents with substantial content")
    return docs

def index_documents():
    docs = load_docs()
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
    print("Splitting documents into chunks...")
    
    split_docs = splitter.split_documents(docs)
    print(f"Split into {len(split_docs)} chunks.")

    print("Initializing Ollama embeddings...")
    embed = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    print("Creating vector database (this may take several minutes)...")
    print("Processing embeddings for chunks...")
    vectordb = Chroma.from_documents(split_docs, embed, persist_directory=CHROMA_DB_DIR)
    
    print(f"✅ Indexed {len(split_docs)} chunks. Vector DB saved to {CHROMA_DB_DIR}")

if __name__ == "__main__":
    index_documents()
