from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from typing import List

def initialize_llm():
    """Initialize the Ollama LLM"""
    return OllamaLLM(
        model="llama3.2",
        temperature=0.3
    )

def generate_response(llm, query: str, context: List[str]) -> str:
    context_str = "\n\n".join([doc.page_content for doc in context])
    
    prompt = ChatPromptTemplate.from_template(
        """You are a smart recruiter assistant. Answer the user's question based on the following context.

        Context:
        {context}

        you will take meny CVS so you need to understand which cv belongs to whom and the skills for each candidate
        I will ask you quetions about the candidate like who is the best in time series 
        or about skills for one candidate and you should replay from the CVs
        Be concise and professional. If you don't know the answer, say you don't know.
        
        Question: {question}
        
        Answer:"""
    )
    
    chain = prompt | llm
    return chain.invoke({"context": context_str, "question": query})