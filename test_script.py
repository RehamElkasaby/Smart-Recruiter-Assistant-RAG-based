from process_files import process_uploaded_files
from process_query import process_query
from vector_store import vector_store_init, add_candidates
from llm_config import llm, embeddings


file_paths = ["CVs/Reham_CV_April_2025[1].pdf","CVs/Hager elkasapy cv.pdf"]
chunks,_ = process_uploaded_files(file_paths)

vector_store = vector_store_init()
add_candidates(vector_store, chunks)


print("*******************************************************")



query = """ what Reham Email address """
response = process_query(query, vector_store=None, llm=llm,file_paths=file_paths)

print("Response:\n", response)