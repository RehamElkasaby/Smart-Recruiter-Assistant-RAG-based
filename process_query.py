%%writefile process_query.py
from vector_store import vector_store_init, search_candidate, get_full_cv
from RAG_engine import initialize_llm, generate_response , generate_response_who , generate_summary_response
from typing import List
from process_files import process_uploaded_files
import os

def process_query(query: str, vector_store=None, llm=None):
    if not vector_store:
        vector_store = vector_store_init()
    if not llm:
        llm = initialize_llm()

    file_paths = ["/content/Mariam-Osama.pdf", "/content/Reham_Elkasaby.pdf","/content/Hager elkasapy.pdf"]
    _, candidate_names = process_uploaded_files(file_paths)

    if is_who_question(query):
        return answer_who_question(query, vector_store, llm, candidate_names)
    if is_summurize(query):
        return answer_summarize(query, vector_store, llm, candidate_names)
    return answer_normal_question(query, vector_store, llm, candidate_names)

#*********************************************************************************

def is_who_question(query: str) -> bool:
    return query.lower().startswith(("who", "which candidate"))

def is_summurize(query: str) -> bool:
    return query.lower().startswith(("summurize", "what skills"))


def answer_who_question(query: str, vector_store, llm, candidate_names: List[str]) -> str:
    print("who")
    sections = search_candidate(
        vector_store,
        query,
        top_k=5,
        filter_by={"document_type": "cv_section"}
    )

    return generate_response_who(llm, query, sections, candidate_names)

def answer_normal_question(query: str, vector_store, llm, candidate_names: List[str]):
    print("normal")
    results = search_candidate(vector_store, query, top_k=5)
    return generate_response(llm, query, results, candidate_names)


def answer_summarize(query: str, vector_store, llm, candidate_names: List[str]) -> str:
    print("summurize")
    full_cvs = []
    print(candidate_names)
    for name in candidate_names:
        print(name)
        results = search_candidate(
            vector_store,
            query,
            top_k=1,
            filter_by={
                "document_type": "full_cv",
                "candidate_name": name
            },
        )

        if results:
            full_cvs.extend(results)
    
    if not full_cvs:
        return "No full CVs found for summarization"
    
    return generate_summary_response(llm, query, full_cvs)