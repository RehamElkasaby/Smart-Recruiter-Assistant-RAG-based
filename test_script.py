from process_files import process_uploaded_files
from process_query import process_query
from vector_store import vector_store_init, add_candidates

file_paths = ["CVs/Mariam-Osama.pdf", "CVs/Reham_Elkasaby.pdf","CVs/Hager elkasapy.pdf"]
chunks,_ = process_uploaded_files(file_paths)

vector_store = vector_store_init()
add_candidates(vector_store, chunks)


print("*******************************************************")


query = """who is suitable for thes job We are seeking a highly motivated AI Engineer 
with a strong focus on OpenAI technologies to join our growing team. The ideal candidate will have a deep understanding of AI models,
multi-agent systems, and the ability to design, develop, and implement intelligent agents capable of autonomous problem-solving and decision-making.
Your work will contribute to creating innovative AI-driven applications and solutions that integrate cutting-edge advancements in artificial intelligence, 
including GPT models, reinforcement learning, and natural language processing."""
response = process_query(query)

print("Response:\n", response)