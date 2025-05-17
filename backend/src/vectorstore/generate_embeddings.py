# backend/vectorstore/generate_embeddings.py
import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_DIR = "data/processed/chunks"
VECTOR_DB_DIR = "data/vector_db"
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(f"sentence-transformers/{MODEL_NAME}")

def load_chunks():
    chunks = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith("_chunks.txt"):
            with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
                chunks.extend(f.read().split("\n---\n"))
    return chunks

def store_faiss():
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)
    chunks = load_chunks()
    embeddings = model.encode(chunks, show_progress_bar=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    faiss.write_index(index, os.path.join(VECTOR_DB_DIR, "faiss_index"))

    with open(os.path.join(VECTOR_DB_DIR, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)

    print(f"✅ Stored {len(chunks)} embeddings in FAISS.")
    return len(chunks)
