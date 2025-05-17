# backend/main.py
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os

# Adjusted import paths due to new folder structure
from src.preprocessing.extract_text import extract_all_pdfs
from src.preprocessing.chunk_text import chunk_all_text_files
from src.vectorstore.generate_embeddings import store_faiss
from src.vectorstore.retrieve import retrieve_chunks

app = FastAPI()

# CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ideally restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== ROUTES ==========

@app.get("/")
def read_root():
    return {"message": "📚 PDFQuery Backend is Live!"}

# 1. Upload PDF
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

# 2. Extract Text
@app.post("/process")
def run_extraction_and_chunking():
    try:
        extracted = extract_all_pdfs()
        chunked = chunk_all_text_files()
        return {"extracted": extracted, "chunked": chunked}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Generate Embeddings
@app.post("/embed")
def generate_embeddings():
    try:
        count = store_faiss()
        return {"status": f"✅ Stored {count} chunks in FAISS."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Query
class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.post("/query")
def query_chunks(req: QueryRequest):
    try:
        results = retrieve_chunks(req.query, top_k=req.top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
