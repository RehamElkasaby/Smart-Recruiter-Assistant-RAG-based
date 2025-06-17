#from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
import os
import shutil
import time
from llm_config import llm, embeddings


def vector_store_init():
    persist_dir = "./chroma_langchain_db"
    if os.path.exists(persist_dir):
        for _ in range(3):  # Retry up to 3 times
            try:
                shutil.rmtree(persist_dir)
                break
            except PermissionError:
                time.sleep(1) 
    
    #embedding = OllamaEmbeddings(model="all-minilm")
    
    return Chroma(
        collection_name="recruiter_candidates",
        persist_directory=persist_dir,
        embedding_function=embeddings 
    )

def add_candidates(vector_store, documents):
    vector_store.add_documents(documents)

def search_candidate(vector_store, query, top_k=3, filter_by=None):
    if filter_by:
        if len(filter_by) > 1:
            filter_by = {"$and": [{k: v} for k, v in filter_by.items()]}
        else:
            filter_by = filter_by
    return vector_store.similarity_search(
        query=query,
        k=top_k,
        filter=filter_by
    )


def get_full_cv(vector_store, cv_name):
    filter_criteria = {
        "$and": [
            {"source": cv_name},
            {"document_type": "full_cv"}
        ]
    }
    results = vector_store.similarity_search(
        query=cv_name,
        k=1,
        filter=filter_criteria
    )
    return results[0] if results else None