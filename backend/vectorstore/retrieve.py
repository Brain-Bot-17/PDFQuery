# backend/vectorstore/retrieve.py
import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

VECTOR_DB_DIR = "data/vector_db"
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(f"sentence-transformers/{MODEL_NAME}")

def retrieve_chunks(query, top_k=3):
    index_path = os.path.join(VECTOR_DB_DIR, "faiss_index")
    chunks_path = os.path.join(VECTOR_DB_DIR, "chunks.pkl")

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        raise FileNotFoundError("FAISS index or chunk file not found. Please run /generate-embeddings first.")

    index = faiss.read_index(index_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    results = [chunks[i] for i in indices[0]]
    return results
