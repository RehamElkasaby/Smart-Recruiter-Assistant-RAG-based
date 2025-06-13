from process_files import process_uploaded_files
from process_query import process_query
from vector_store import vector_store_init, add_candidates

file_paths = ["CVs/Mariam-Osama.pdf", "CVs/Reham_Elkasaby.pdf","CVs/Hager elkasapy.pdf"]
chunks,_ = process_uploaded_files(file_paths)

vector_store = vector_store_init()
add_candidates(vector_store, chunks)

query = "what skills does Mariam Osama"
response = process_query(query)

print("Response:\n", response)
print("*******************************************************")

query = "who candidate can you recommended as junior AI developer"
response = process_query(query)

print("Response:\n", response)
print("*******************************************************")


query = "what is the phone number of reham"
response = process_query(query)

print("Response:\n", response)