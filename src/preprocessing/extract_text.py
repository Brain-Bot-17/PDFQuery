import os
import fitz  # PyMuPDF
import pdfplumber

DATA_DIR = "data/raw"
OUTPUT_DIR = "data/processed/"

def extract_text_pymupdf(pdf_path):
    """Extract text from PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text

def extract_text_pdfplumber(pdf_path):
    """Extract text from PDF using pdfplumber."""
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    return text

def process_pdfs():
    """Process all PDFs in the raw data folder."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(DATA_DIR, filename)
            text = extract_text_pymupdf(pdf_path)  # Try PyMuPDF
            if not text.strip():
                text = extract_text_pdfplumber(pdf_path)  # Fallback

            output_file = os.path.join(OUTPUT_DIR, f"{filename}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"✅ Processed: {filename}")

if __name__ == "__main__":
    process_pdfs()
