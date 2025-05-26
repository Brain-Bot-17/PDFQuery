# backend/vectorstore/generate_embeddings.py

import os
import faiss
import pickle
import numpy as np

DATA_DIR = "data/processed/chunks"
VECTOR_DB_DIR = "data/vector_db"
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"
BATCH_SIZE = 32  # adjust for Render memory

def load_chunks():
    chunks = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith("_chunks.txt"):
            file_path = os.path.join(DATA_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                parts = [chunk.strip() for chunk in f.read().split("\n---\n") if chunk.strip()]
                chunks.extend(parts)
    return chunks

def store_faiss():
    try:
        from sentence_transformers import SentenceTransformer  # lazy import
        model = SentenceTransformer(MODEL_NAME)

        os.makedirs(VECTOR_DB_DIR, exist_ok=True)
        chunks = load_chunks()

        if not chunks:
            raise ValueError("No chunks found. Did you run /process?")

        print(f"🔢 Encoding {len(chunks)} chunks in batches of {BATCH_SIZE}...")

        embeddings = []
        for i in range(0, len(chunks), BATCH_SIZE):
            batch = chunks[i:i + BATCH_SIZE]
            batch_embeddings = model.encode(
                batch,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True  # Optional: helps in L2 similarity
            ).astype("float32")
            embeddings.append(batch_embeddings)

        all_embeddings = np.vstack(embeddings)

        print(f"✅ Finished encoding. Building FAISS index with shape: {all_embeddings.shape}")
        index = faiss.IndexFlatL2(all_embeddings.shape[1])
        index.add(all_embeddings)

        faiss.write_index(index, os.path.join(VECTOR_DB_DIR, "faiss_index"))
        with open(os.path.join(VECTOR_DB_DIR, "chunks.pkl"), "wb") as f:
            pickle.dump(chunks, f)

        print(f"✅ Stored {len(chunks)} embeddings in FAISS.")
        return len(chunks)

    except Exception as e:
        print("❌ Error in store_faiss():", e)
        raise
