from vector_store import vector_store_init, search_candidate, get_full_cv, add_candidates
from RAG_engin import initialize_llm, generate_response, generate_response_who, generate_summary_response
from typing import List
from process_files import process_uploaded_files
import os
from langchain_tavily import TavilySearch


# Global flag to track if documents have been added
DOCUMENTS_ADDED = False

def process_query(query: str, vector_store=None, llm=None):
    global DOCUMENTS_ADDED
    
    if not vector_store:
        vector_store = vector_store_init()
    if not llm:
        llm = initialize_llm()
    
    file_paths = ["CVs/Mariam-Osama.pdf", "CVs/Reham_Elkasaby.pdf", "CVs/Hager elkasapy.pdf"]
    
    # Only add documents once per session
    if not DOCUMENTS_ADDED:
        chunks, candidate_names = process_uploaded_files(file_paths)
        add_candidates(vector_store, chunks)
        DOCUMENTS_ADDED = True
    else:
        _, candidate_names = process_uploaded_files(file_paths)
    
    if is_who_question(query):
        return answer_who_question(query, vector_store, llm, candidate_names)
    if is_summurize(query):
        return answer_summarize(query, vector_store, llm, candidate_names)
    if is_find_job(query):
        summary = answer_summarize(query, vector_store, llm, candidate_names)
        print(summary)
        return answer_recommend_jobs(summary, llm)
    return answer_normal_question(query, vector_store, llm,candidate_names)


#*********************************************************************************

def is_who_question(query: str) -> bool:
    return query.lower().startswith(("who", "which candidate"))

def is_summurize(query: str) -> bool:
    return query.lower().startswith(("summurize", "what skills"))

def is_find_job(query: str) -> bool:
    return query.lower().startswith(("find job"))

#*********************************************************************************

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
                "candidate_name": name
            },
        )

        if results:
            full_cvs.extend(results)
    
    if not full_cvs:
        return "No full CVs found for summarization"
    
    return generate_summary_response(llm, query, full_cvs)
    

def answer_recommend_jobs(summary: str, llm, k: int = 6) -> List[dict]:
    os.environ["TAVILY_API_KEY"] = "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"
    tavily = TavilySearch(
        max_results=5,
        search_depth="advanced"
    )

    prompt = f"""Based on this summary, generate {k} job search queries:
    {summary}
    Return ONLY the queries, one per line, no numbering."""
    
    response = llm.invoke(prompt)
    queries_text = response if isinstance(response, str) else response.content
    queries = [q.strip() for q in queries_text.split('\n') if q.strip()][:k]
    
    results = []
    for query in queries:
        try:
            search_results = tavily.invoke(query)
            
            if isinstance(search_results, str):
                print(f"Search API returned error: {search_results}")
                continue
                
            if isinstance(search_results, dict) and "results" in search_results:
                for r in search_results.get("results", [])[:2]:
                    if isinstance(r, dict): 
                        results.append({
                            "title": r.get("title", "Job Opportunity"),
                            "url": r.get("url", "#"),
                        })
                    
            else:
                print(f"Unexpected search results format: {type(search_results)}")
        except Exception as e:
            print(f"Search error for query '{query}': {e}")
    
    return results[:10]  # Return max 5 jobs