# process_query.py (updated)
from vector_store import vector_store_init, search_candidate, get_full_cv
from RAG_engin import initialize_llm, generate_response , generate_response_who , generate_summary_response
from typing import List
from process_files import process_uploaded_files
import os

def process_query(query: str, vector_store=None, llm=None):
    if not vector_store:
        vector_store = vector_store_init()
    if not llm:
        llm = initialize_llm()
    
    file_paths = ["CVs/Mariam-Osama.pdf", "CVs/Reham_Elkasaby.pdf"]
    _, candidate_names = process_uploaded_files(file_paths)
    
    if is_who_question(query):
        return answer_who_question(query, vector_store, llm, candidate_names)
    if is_summurize(query):
        return answer_summurize(query, vector_store, llm)
    return answer_normal_question(query, vector_store, llm, candidate_names)

#*********************************************************************************

def is_who_question(query: str) -> bool:
    return query.lower().startswith(("who", "which candidate"))

def is_summurize(query: str) -> bool:
    return query.lower().startswith(("summurize", "what skills"))


def answer_who_question(query: str, vector_store, llm, candidate_names: List[str]) -> str:
    # Search using the question directly
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


def answer_summurize(query: str, vector_store, llm) -> str:
    candidate_names = [name.strip() for name in query.split(" or ")[-1].split("?")[0].split()]

    sections = []
    for name in candidate_names:
        sections.extend(search_candidate(
            vector_store,
            name,
            top_k=3,
            filter_by={"document_type": "cv_section"}
        ))

    cv_contexts = []
    seen_cvs = set()
    for section in sections:
        cv_name = section.metadata["source"]
        if cv_name not in seen_cvs:
            full_cv = get_full_cv(vector_store, cv_name)
            if full_cv:
                cv_contexts.append(full_cv)
                seen_cvs.add(cv_name)
    print(cv_contexts)

    return generate_summary_response(llm, query, cv_contexts)