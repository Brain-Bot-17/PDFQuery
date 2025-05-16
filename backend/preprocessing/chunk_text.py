# backend/preprocessing/chunk_text.py

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

DATA_DIR = "data/processed"
OUTPUT_DIR = "data/processed/chunks"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def chunk_text(text, chunk_size=512, overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap
    )
    return splitter.split_text(text)

def chunk_all_text_files():
    results = []
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
            results.append((filename, len(chunks)))
    return results

