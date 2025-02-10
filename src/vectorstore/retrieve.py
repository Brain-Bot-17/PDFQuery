import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

VECTOR_DB_DIR = "data/vector_db"
MODEL_NAME = "all-MiniLM-L6-v2"

# Load model and FAISS index
model = SentenceTransformer(f"sentence-transformers/{MODEL_NAME}")
index = faiss.read_index(os.path.join(VECTOR_DB_DIR, "faiss_index"))

# Load chunk mappings
with open(os.path.join(VECTOR_DB_DIR, "chunks.pkl"), "rb") as f:
    chunks = pickle.load(f)

def retrieve(query, top_k=3):
    """Retrieve top-k relevant text chunks for a given query."""
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)

    results = [chunks[i] for i in indices[0]]
    return results

if __name__ == "__main__":
    query = input("Enter a query: ")
    results = retrieve(query)
    
    print("\n🔍 **Top Matches:**")
    for i, res in enumerate(results, 1):
        print(f"{i}. {res}\n")
