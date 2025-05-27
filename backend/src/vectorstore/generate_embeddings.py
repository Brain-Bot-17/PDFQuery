import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

PROCESSED_DIR = "data/processed"
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"
BATCH_SIZE = 32

def load_chunks(chunk_file):
    with open(chunk_file, "r", encoding="utf-8") as f:
        return [c.strip() for c in f.read().split("\n---\n") if c.strip()]

def store_faiss_per_pdf():
    model = SentenceTransformer(MODEL_NAME)
    pdf_dirs = [d for d in os.listdir(PROCESSED_DIR) if os.path.isdir(os.path.join(PROCESSED_DIR, d))]

    for pdf_name in pdf_dirs:
        pdf_path = os.path.join(PROCESSED_DIR, pdf_name)
        chunk_file = os.path.join(pdf_path, "chunks.txt")

        if not os.path.exists(chunk_file):
            print(f"⚠️ Skipping '{pdf_name}': No chunks.txt")
            continue

        print(f"🔢 Processing chunks for: {pdf_name}")
        chunks = load_chunks(chunk_file)

        if not chunks:
            print(f"⚠️ Skipping '{pdf_name}': No non-empty chunks")
            continue

        embeddings = []
        for i in range(0, len(chunks), BATCH_SIZE):
            batch = chunks[i:i + BATCH_SIZE]
            emb = model.encode(
                batch,
                convert_to_numpy=True,
                show_progress_bar=False,
                normalize_embeddings=True
            ).astype("float32")
            embeddings.append(emb)

        all_embeddings = np.vstack(embeddings)
        index = faiss.IndexFlatL2(all_embeddings.shape[1])
        index.add(all_embeddings)

        # Save index and chunks separately per PDF
        faiss.write_index(index, os.path.join(pdf_path, "index.faiss"))
        with open(os.path.join(pdf_path, "embeddings.pkl"), "wb") as f:
            pickle.dump(chunks, f)

        print(f"✅ Stored FAISS index and embeddings for: {pdf_name}")

    print("✅ All PDFs processed successfully.")
