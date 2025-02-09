import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Define absolute paths
DATA_DIR = "C:/Users/HP/OneDrive/Desktop/GenieRAG/data/processed/chunks/"
VECTOR_DB_DIR = "C:/Users/HP/OneDrive/Desktop/GenieRAG/data/vector_db/"
MODEL_NAME = "all-MiniLM-L6-v2"

# Load sentence transformer model
model = SentenceTransformer(f"sentence-transformers/{MODEL_NAME}")

def load_chunks():
    """Load chunked text files."""
    chunks = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith("_chunks.txt"):
            with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
                chunks.extend(f.read().split("\n---\n"))
    return chunks

def store_faiss():
    """Convert text to embeddings and store in FAISS."""
    chunks = load_chunks()
    embeddings = model.encode(chunks, show_progress_bar=True)

    # Store embeddings in FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])  # L2 distance
    index.add(np.array(embeddings))

    # Save index
    faiss.write_index(index, os.path.join(VECTOR_DB_DIR, "faiss_index"))
    
    # Save chunks mapping
    with open(os.path.join(VECTOR_DB_DIR, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)
    
    print(f"✅ Stored {len(chunks)} embeddings in FAISS.")

if __name__ == "__main__":
    store_faiss()
