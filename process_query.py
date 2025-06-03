from vector_store import vector_store_init, search_candidate, get_full_cv
from RAG_engin import initialize_llm, generate_response
from typing import List

def process_query(query: str, vector_store=None, llm=None):
    if not vector_store:
        vector_store = vector_store_init()
    if not llm:
        llm = initialize_llm()
    
    if is_who_question(query):
        return answer_who_question(query, vector_store, llm)
    return answer_normal_question(query, vector_store, llm)

def is_who_question(query: str) -> bool:
    return query.lower().startswith(("who", "which candidate"))

def answer_who_question(query: str, vector_store, llm) -> str:
    # Extract candidate names from query
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
    
    return generate_response(llm, query, cv_contexts)

def answer_normal_question(query: str, vector_store, llm):
    results = search_candidate(vector_store, query)  # Fixed function name
    return generate_response(llm, query, results)