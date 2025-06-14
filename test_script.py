from process_files import process_uploaded_files
from process_query import process_query
from vector_store import vector_store_init, add_candidates

file_paths = ["CVs/Mariam-Osama.pdf", "CVs/Reham_Elkasaby.pdf","CVs/Hager elkasapy.pdf"]
chunks,_ = process_uploaded_files(file_paths)

vector_store = vector_store_init()
add_candidates(vector_store, chunks)


print("*******************************************************")



query = """ what Mariam Osama Email address """
response = process_query(query)

print("Response:\n", response)