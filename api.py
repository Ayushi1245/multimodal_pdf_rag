"""
FastAPI backend for the Multimodal RAG React frontend.

Thin REST API that wraps the existing ingest.py and rag_chain.py pipeline.
Run with: uvicorn api:app --reload --port 8000
"""

import os
import json
import shutil
import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import config
import ingest
import rag_chain

app = FastAPI(
    title="Multimodal RAG API",
    description="REST API for multimodal PDF document Q&A powered by Groq.",
    version="1.0.0",
)

# CORS — allow Vite dev server and common local origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request / Response Models ───────────────────────────────────────────────

class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[dict]
    image_refs: list[dict]


class StatsResponse(BaseModel):
    document_count: int
    chunk_count: int


class UploadResponse(BaseModel):
    file_name: str
    text_chunks: int
    image_chunks: int
    message: str


# ─── Endpoints ───────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {"service": "Multimodal RAG API", "status": "healthy"}


@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """Get document and chunk counts."""
    try:
        retriever = ingest.get_retriever()
        chunk_count = retriever.vectorstore._collection.count()
    except Exception:
        chunk_count = 0

    sources = _get_indexed_sources()
    return StatsResponse(document_count=len(sources), chunk_count=chunk_count)


@app.get("/api/documents")
async def list_documents():
    """List all indexed document names."""
    return {"documents": _get_indexed_sources()}


@app.post("/api/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and ingest a PDF document."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Only PDF files are accepted.")

    # Save to temp file
    content = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        text_chunks, image_chunks = ingest.ingest_pdf(tmp_path)
        return UploadResponse(
            file_name=file.filename,
            text_chunks=text_chunks,
            image_chunks=image_chunks,
            message=f"Indexed {text_chunks} text chunks and {image_chunks} image summaries.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
    finally:
        os.unlink(tmp_path)


@app.delete("/api/documents/{file_name}")
async def delete_document(file_name: str):
    """Delete a specific document from the index."""
    sources = _get_indexed_sources()
    if file_name not in sources:
        raise HTTPException(status_code=404, detail=f"Document '{file_name}' not found.")

    success = ingest.delete_file(file_name)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete document.")

    return {"message": f"Deleted '{file_name}'"}


@app.post("/api/ask", response_model=AskResponse)
async def ask_question(req: AskRequest):
    """Ask a question about the indexed documents."""
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    sources = _get_indexed_sources()
    if not sources:
        return AskResponse(
            answer="No documents indexed yet. Please upload and process a PDF first.",
            sources=[],
            image_refs=[],
        )

    try:
        result = rag_chain.ask_question(req.question)

        # Serialize LangChain Document objects to plain dicts
        serialized_sources = []
        for doc in result.get("sources", []):
            serialized_sources.append({
                "content": doc.page_content[:500],
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "?"),
                "type": doc.metadata.get("type", "text"),
            })

        return AskResponse(
            answer=result["answer"],
            sources=serialized_sources,
            image_refs=result.get("image_refs", []),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.delete("/api/index")
async def clear_index():
    """Clear the entire index (all documents, chunks, cache)."""
    try:
        if os.path.exists(config.CHROMA_PERSIST_DIR):
            shutil.rmtree(config.CHROMA_PERSIST_DIR)
        if os.path.exists(ingest.DOCSTORE_DIR):
            shutil.rmtree(ingest.DOCSTORE_DIR)
        if os.path.exists(ingest.CACHE_FILE):
            os.remove(ingest.CACHE_FILE)

        # Recreate directories
        os.makedirs(config.CHROMA_PERSIST_DIR, exist_ok=True)

        return {"message": "Index cleared successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear index: {str(e)}")


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _get_indexed_sources() -> list[str]:
    """Read the ingested files cache."""
    if os.path.exists(ingest.CACHE_FILE):
        try:
            with open(ingest.CACHE_FILE) as f:
                return list(json.load(f).keys())
        except Exception:
            pass
    return []


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
