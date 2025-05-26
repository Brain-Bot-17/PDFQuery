# backend/preprocessing/chunk_text.py

import os

DATA_DIR = "data/processed"
OUTPUT_DIR = "data/processed/chunks"

DEFAULT_CHUNK_SIZE = 512
DEFAULT_OVERLAP = 50

os.makedirs(OUTPUT_DIR, exist_ok=True)

def chunk_text(text, chunk_size=DEFAULT_CHUNK_SIZE, overlap=DEFAULT_OVERLAP):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap
    )
    return splitter.split_text(text)

def chunk_all_text_files():
    results = []

    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(DATA_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not text:
            continue  # Skip empty files

        chunks = chunk_text(text)

        if not chunks:
            continue

        chunk_file_path = os.path.join(OUTPUT_DIR, f"{filename}_chunks.txt")
        with open(chunk_file_path, "w", encoding="utf-8") as out_f:
            out_f.write("\n---\n".join(chunks))

        results.append((filename, len(chunks)))

    return results
