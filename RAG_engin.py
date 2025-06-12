# RAG_engine.py (updated)
import os
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from typing import List

def initialize_llm():
    return OllamaLLM(
        model="llama3.2",
        temperature=0
    )

def generate_response_who(llm, query: str, context: List, candidate_names: List[str]) -> str:
    # Format context with candidate names
    context_str = ""
    for doc in context:
        name = doc.metadata.get("candidate_name", "Unknown Candidate")
        context_str += f"--- CANDIDATE: {name} ---\n{doc.page_content}\n\n"
    
    valid_names = ", ".join(candidate_names)
    
    prompt = ChatPromptTemplate.from_template(
        """
        **Role**: You are an AI Recruiting Assistant that matches CVs to job descriptions with explainable rankings.  
        Important Rules:
        1. ONLY use these candidate names: {valid_names}
        2. NEVER invent new names or use names not in this list
        3. If a name isn't in the context, say "I don't have information about that candidate"
        4. For comparison questions, list candidates using ONLY names from the valid list

        **Task**:  
        1. Analyze the provided job description and candidate CVs.  
        2. Rank candidates from best to worst fit (Top K={K}).  
        3. For each candidate, provide:  
        - **Match Score (%)**: Overall fit for the role.  
        - **Key Strengths**: 3-5 bullet points aligning with the job requirements.  
        - **Potential Gaps**: Missing skills/experience (if any).  
        - **Recommendation**: "Strong Fit," "Moderate Fit," or "Weak Fit."  

        **Inputs**:  
        - Job Description: "{question}"  
        - Candidate CVs:  
        {context}  

        **Scoring Criteria**:  
        1. **Skill Match** (Weight: 40%):  
        - Exact matches to required skills.  
        - Related/transferable skills.  
        2. **Experience Level** (Weight: 30%):  
        - Years in relevant roles.  
        - Seniority (e.g., "Led teams" vs. "Contributed to projects").  
        3. **Educational Relevance** (Weight: 20%):  
        - Degree/credentials matching job requirements.  
        - Certifications or specialized training.  
        4. **Other Factors** (Weight: 10%):  
        - Industry-specific keywords.  
        - Cultural fit (e.g., startups vs. corporate).  

        **Output Format**:  
        ### **Top Candidates for [Job Title]**  
        #### **1. [Candidate Name]**  
        - **Match Score**: 92%  
        - **Key Strengths**:  
        - 5+ years of Python (exact match for "Senior Python Developer").  
        - Led 3 machine learning projects (matches "team leadership" requirement).  
        - MSc in Computer Science (exact degree match).  
        - **Potential Gaps**:  
        - Limited cloud experience (AWS/Azure not mentioned).  
        - **Recommendation**: ✅ Strong Fit  

        #### **2. [Candidate Name]**  
        - **Match Score**: 75%  
        ...  

        **Rules**:  
        - Never invent skills/experiences. Say "Not mentioned" for gaps.  
        - Prioritize candidates with exact skill matches.  
        - Explain scores transparently (e.g., "+20% for Python expertise").  """
    )
    
    chain = prompt | llm
    return chain.invoke({
        "context": context_str, 
        "question": query,
        "valid_names": valid_names,
        "K" : 3
    })

def Response_summurize_skills(llm, query: str, context: List, candidate_names: List[str]) -> str:
    # Format context with candidate names
    context_str = ""
    for doc in context:
        name = doc.metadata.get("candidate_name", "Unknown Candidate")
        context_str += f"--- CANDIDATE: {name} ---\n{doc.page_content}\n\n"
    
    valid_names = ", ".join(candidate_names)
    
    prompt = ChatPromptTemplate.from_template(
        """
        **Role**: You are an AI Recruiting Assistant that matches CVs to job descriptions with explainable rankings.  
        Important Rules:
        1. ONLY use these candidate names: {valid_names}
        2. NEVER invent new names or use names not in this list
        3. If a name isn't in the context, say "I don't have information about that candidate"
        4. For comparison questions, list candidates using ONLY names from the valid list

        **Task**:  
        1. Analyze the provided job description and candidate CVs.  
        2. Rank candidates from best to worst fit (Top K={K}).  
        3. For each candidate, provide:  
        - **Match Score (%)**: Overall fit for the role.  
        - **Key Strengths**: 3-5 bullet points aligning with the job requirements.  
        - **Potential Gaps**: Missing skills/experience (if any).  
        - **Recommendation**: "Strong Fit," "Moderate Fit," or "Weak Fit."  

        **Inputs**:  
        - Job Description: "{question}"  
        - Candidate CVs:  
        {context}  

        **Scoring Criteria**:  
        1. **Skill Match** (Weight: 40%):  
        - Exact matches to required skills.  
        - Related/transferable skills.  
        2. **Experience Level** (Weight: 30%):  
        - Years in relevant roles.  
        - Seniority (e.g., "Led teams" vs. "Contributed to projects").  
        3. **Educational Relevance** (Weight: 20%):  
        - Degree/credentials matching job requirements.  
        - Certifications or specialized training.  
        4. **Other Factors** (Weight: 10%):  
        - Industry-specific keywords.  
        - Cultural fit (e.g., startups vs. corporate).  

        **Output Format**:  
        ### **Top Candidates for [Job Title]**  
        #### **1. [Candidate Name]**  
        - **Match Score**: 92%  
        - **Key Strengths**:  
        - 5+ years of Python (exact match for "Senior Python Developer").  
        - Led 3 machine learning projects (matches "team leadership" requirement).  
        - MSc in Computer Science (exact degree match).  
        - **Potential Gaps**:  
        - Limited cloud experience (AWS/Azure not mentioned).  
        - **Recommendation**: ✅ Strong Fit  

        #### **2. [Candidate Name]**  
        - **Match Score**: 75%  
        ...  

        **Rules**:  
        - Never invent skills/experiences. Say "Not mentioned" for gaps.  
        - Prioritize candidates with exact skill matches.  
        - Explain scores transparently (e.g., "+20% for Python expertise").  """
    )
    
    chain = prompt | llm
    return chain.invoke({
        "context": context_str, 
        "question": query,
        "valid_names": valid_names,
        "K" : 3
    })