# backend/vectorstore/generate_embeddings.py

import os
import faiss
import pickle
import numpy as np

DATA_DIR = "data/processed/chunks"
VECTOR_DB_DIR = "data/vector_db"
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"
BATCH_SIZE = 32  # adjustable depending on memory limits

def load_chunks():
    chunks = []
    for filename in os.listdir(DATA_DIR):
        if not filename.endswith("_chunks.txt"):
            continue
        file_path = os.path.join(DATA_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            chunks.extend([chunk.strip() for chunk in f.read().split("\n---\n") if chunk.strip()])
    return chunks

def store_faiss():
    from sentence_transformers import SentenceTransformer  # delayed import
    model = SentenceTransformer(MODEL_NAME)

    os.makedirs(VECTOR_DB_DIR, exist_ok=True)

    chunks = load_chunks()
    if not chunks:
        return 0

    embeddings = []
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        batch_embeddings = model.encode(batch, show_progress_bar=False, convert_to_numpy=True)
        embeddings.append(batch_embeddings)

    all_embeddings = np.vstack(embeddings)

    index = faiss.IndexFlatL2(all_embeddings.shape[1])
    index.add(all_embeddings)
    faiss.write_index(index, os.path.join(VECTOR_DB_DIR, "faiss_index"))

    with open(os.path.join(VECTOR_DB_DIR, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)

    return len(chunks)
