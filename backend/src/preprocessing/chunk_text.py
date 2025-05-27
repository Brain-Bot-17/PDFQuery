import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

PROCESSED_DIR = "data/processed"
DEFAULT_CHUNK_SIZE = 512
DEFAULT_OVERLAP = 50

def chunk_text(text, chunk_size=DEFAULT_CHUNK_SIZE, overlap=DEFAULT_OVERLAP):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap
    )
    return splitter.split_text(text)

def chunk_all_text_files():
    results = []

    for folder in os.listdir(PROCESSED_DIR):
        folder_path = os.path.join(PROCESSED_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        text_file_path = os.path.join(folder_path, "full_text.txt")
        if not os.path.exists(text_file_path):
            continue

        with open(text_file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not text:
            continue

        chunks = chunk_text(text)
        if not chunks:
            continue

        # Save chunks in same directory
        chunk_file_path = os.path.join(folder_path, "chunks.txt")
        with open(chunk_file_path, "w", encoding="utf-8") as out_f:
            out_f.write("\n---\n".join(chunks))

        results.append((folder, len(chunks)))

    return results
