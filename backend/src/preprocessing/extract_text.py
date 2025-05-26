# backend/preprocessing/extract_text.py

import os

DATA_DIR = "data/raw"
OUTPUT_DIR = "data/processed"

def extract_text_pymupdf(pdf_path):
    try:
        import fitz  # PyMuPDF
        with fitz.open(pdf_path) as doc:
            for page in doc:
                yield page.get_text("text")
    except Exception:
        yield ""  # fallback

def extract_text_pdfplumber(pdf_path):
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                yield page.extract_text() or ""
    except Exception:
        yield ""

def extract_all_pdfs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    processed_files = []

    for filename in os.listdir(DATA_DIR):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(DATA_DIR, filename)
        output_file = os.path.join(OUTPUT_DIR, f"{filename}.txt")

        # Try PyMuPDF first
        text_gen = extract_text_pymupdf(pdf_path)
        text = "\n".join(text_gen).strip()

        # Fallback to pdfplumber if empty
        if not text:
            text = "\n".join(extract_text_pdfplumber(pdf_path)).strip()

        if not text:
            continue  # Skip empty PDFs

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)

        processed_files.append(filename)

    return processed_files
