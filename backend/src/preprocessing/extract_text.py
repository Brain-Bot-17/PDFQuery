import os
import fitz  # PyMuPDF
import pdfplumber

DATA_DIR = "data/raw"
OUTPUT_ROOT = "data/processed"

def extract_text_from_pdf(pdf_path):
    """Try PyMuPDF, fallback to pdfplumber."""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text = page.get_text("text")
                if text:
                    yield text
    except Exception:
        pass

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    yield text
    except Exception:
        pass

def save_text_for_pdf(pdf_filename):
    pdf_path = os.path.join(DATA_DIR, pdf_filename)
    base_name = os.path.splitext(pdf_filename)[0]
    output_dir = os.path.join(OUTPUT_ROOT, base_name)

    os.makedirs(output_dir, exist_ok=True)
    text_output_path = os.path.join(output_dir, "full_text.txt")

    with open(text_output_path, "w", encoding="utf-8") as f:
        for page_text in extract_text_from_pdf(pdf_path):
            f.write(page_text.strip() + "\n\n")

    return output_dir

def extract_all_pdfs():
    os.makedirs(OUTPUT_ROOT, exist_ok=True)
    processed = []

    for filename in os.listdir(DATA_DIR):
        if filename.lower().endswith(".pdf"):
            save_text_for_pdf(filename)
            processed.append(filename)

    return processed
