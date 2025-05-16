# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

# Preprocessing logic
from preprocessing.extract_text import extract_all_pdfs
from preprocessing.chunk_text import chunk_all_text_files

# Vectorstore logic
from vectorstore.generate_embeddings import store_faiss
from vectorstore.retrieve import retrieve_chunks

app = FastAPI()

# ========== ROUTES ==========

@app.get("/")
def read_root():
    return {"message": "📚 PDFQuery Backend is Live!"}

# 1. Extract Text
@app.post("/extract-text")
def run_extraction():
    try:
        processed_files = extract_all_pdfs()
        return {"processed": processed_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Chunk Text
@app.post("/chunk-text")
def run_chunking():
    try:
        chunked_files = chunk_all_text_files()
        return {"chunked": chunked_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Generate Embeddings
@app.post("/generate-embeddings")
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
