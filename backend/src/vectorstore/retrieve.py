import os
import faiss
import pickle
import numpy as np

MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"
PROCESSED_DIR = "data/processed"

def retrieve_chunks(query: str, pdf_name: str, top_k: int = 3):
    pdf_path = os.path.join(PROCESSED_DIR, pdf_name)
    index_path = os.path.join(pdf_path, "index.faiss")
    chunks_path = os.path.join(pdf_path, "embeddings.pkl")

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        raise FileNotFoundError(f"❌ Required files not found for PDF '{pdf_name}'. Run /embed first.")

    # Lazy import
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL_NAME)

    # Load the FAISS index and chunk metadata
    index = faiss.read_index(index_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    # Encode the query
    query_embedding = model.encode([query], convert_to_numpy=True, normalize_embeddings=True).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i in indices[0]:
        if 0 <= i < len(chunks):
            results.append(chunks[i])

    return results
