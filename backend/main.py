from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os

from src.preprocessing.extract_text import extract_text_from_pdf
from src.preprocessing.chunk_text import chunk_text_file
from src.vectorstore.generate_embeddings import store_faiss_for_pdf
from src.vectorstore.retrieve import retrieve_chunks

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== ROUTES ==========

@app.get("/")
def read_root():
    return {"message": "📚 PDFQuery Backend is Live!"}

# Upload PDF
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    try:
        upload_dir = "data/raw"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Process (extract + chunk)
@app.post("/process")
def process_pdf(pdf_name: str = Form(...)):
    try:
        extracted = extract_text_from_pdf(pdf_name)
        chunked = chunk_text_file(pdf_name)
        return {"extracted": extracted, "chunks": chunked}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Generate Embeddings
@app.post("/embed")
def generate_embeddings(pdf_name: str = Form(...)):
    try:
        count = store_faiss_for_pdf(pdf_name)
        return {"status": f"✅ Stored {count} chunks in FAISS for {pdf_name}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Query
class QueryRequest(BaseModel):
    query: str
    pdf_name: str
    top_k: int = 3

@app.post("/query")
def query_pdf(req: QueryRequest):
    try:
        results = retrieve_chunks(req.query, req.pdf_name, top_k=req.top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
