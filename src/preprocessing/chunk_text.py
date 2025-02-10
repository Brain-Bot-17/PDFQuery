import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

DATA_DIR = "data/processed"
OUTPUT_DIR = "data/processed/chunks"

# Create output directory if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def chunk_text(text, chunk_size=512, overlap=50):
    """Split text into chunks for RAG processing."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap
    )
    return splitter.split_text(text)

def process_text_files():
    """Chunk all processed text files."""
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(DATA_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = chunk_text(text)
            chunk_file = os.path.join(OUTPUT_DIR, f"{filename}_chunks.txt")

            with open(chunk_file, "w", encoding="utf-8") as f:
                for chunk in chunks:
                    f.write(chunk + "\n---\n")

            print(f"✅ Chunked: {filename} into {len(chunks)} chunks")

if __name__ == "__main__":
    process_text_files()
