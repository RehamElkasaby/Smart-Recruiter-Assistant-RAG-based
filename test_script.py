from process_files import process_uploaded_files
from process_query import process_query
from vector_store import vector_store_init, add_candidates  # Fixed import

# Step 1: Process documents
file_paths = ["CVs/Mariam-Osama.pdf", "CVs/Reham_Elkasaby.pdf"]
chunks = process_uploaded_files(file_paths)

# Step 2: Add to vector store
vector_store = vector_store_init()
add_candidates(vector_store, chunks)  # Add documents to store

# Step 3: Query
query = "Who has experience with Python programming, Mariam or Reham?"
response = process_query(query)

print("Response:\n", response)