# backend/preprocessing/extract_text.py

import os
import fitz  # PyMuPDF
import pdfplumber

DATA_DIR = "data/raw"
OUTPUT_DIR = "data/processed"

def extract_text_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text

def extract_text_pdfplumber(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    return text

def extract_all_pdfs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(DATA_DIR, filename)
            text = extract_text_pymupdf(pdf_path)
            if not text.strip():
                text = extract_text_pdfplumber(pdf_path)
            output_file = os.path.join(OUTPUT_DIR, f"{filename}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
            results.append(filename)
    return results
