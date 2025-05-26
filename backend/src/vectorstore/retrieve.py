# backend/vectorstore/retrieve.py

import os
import faiss
import pickle
import numpy as np

VECTOR_DB_DIR = "data/vector_db"
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"

def retrieve_chunks(query: str, top_k: int = 3):
    index_path = os.path.join(VECTOR_DB_DIR, "faiss_index")
    chunks_path = os.path.join(VECTOR_DB_DIR, "chunks.pkl")

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        raise FileNotFoundError("🔍 FAISS index or chunks file not found. Run /embed first.")

    # Delayed import and model loading
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL_NAME)

    # Load vector index and chunk data
    index = faiss.read_index(index_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    # Encode query and convert to correct shape/dtype
    query_embedding = model.encode([query], convert_to_numpy=True).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    # Safely retrieve matching chunks
    results = []
    for i in indices[0]:
        if 0 <= i < len(chunks):
            results.append(chunks[i])

    return results
