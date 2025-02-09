import os
import chromadb
from sentence_transformers import SentenceTransformer

DATA_DIR = "C:/Users/HP/OneDrive/Desktop/GenieRAG/data/processed/chunks/"
VECTOR_DB_DIR = "C:/Users/HP/OneDrive/Desktop/GenieRAG/data/vector_db/"
MODEL_NAME = "all-MiniLM-L6-v2"

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
collection = chroma_client.get_or_create_collection(name="rag_collection")

# Load sentence transformer model
model = SentenceTransformer(f"sentence-transformers/{MODEL_NAME}")

def store_chroma():
    """Store text chunks in ChromaDB."""
    chunks = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith("_chunks.txt"):
            with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
                chunks.extend(f.read().split("\n---\n"))

    embeddings = model.encode(chunks, show_progress_bar=True)

    # Add to ChromaDB
    for i, (text, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(ids=[str(i)], embeddings=[embedding.tolist()], documents=[text])

    print(f"✅ Stored {len(chunks)} embeddings in ChromaDB.")

if __name__ == "__main__":
    store_chroma()
