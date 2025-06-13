%%writefile test_script.py
from process_files import process_uploaded_files
from process_query import process_query
from vector_store import vector_store_init, add_candidates

file_paths = ["/content/Mariam-Osama.pdf", "/content/Reham_Elkasaby.pdf","/content/Hager elkasapy.pdf"]
chunks,_ = process_uploaded_files(file_paths)

vector_store = vector_store_init()
add_candidates(vector_store, chunks)

 does Mariam Osama"
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