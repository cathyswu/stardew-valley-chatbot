from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from config import CHROMA_DB_DIR, LLM_MODEL, EMBEDDING_MODEL

def get_rag_chain():
    vectordb = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=OllamaEmbeddings(model=EMBEDDING_MODEL)
    )
    
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    llm = OllamaLLM(model=LLM_MODEL)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")