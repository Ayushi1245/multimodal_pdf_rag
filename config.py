"""
Configuration module for the Multimodal RAG application.
Loads environment variables and defines constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ─── API Keys ────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# ─── Model Configuration ─────────────────────────────────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
SUMMARIZER_MODEL = "llama-3.2-11b-vision-preview"      # Used for image summarization
ANSWER_MODEL = "llama-3.3-70b-versatile"               # Used for final answer generation

# ─── Data Storage ────────────────────────────────────────────────────────────
CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
CHROMA_COLLECTION_NAME = "multimodal_rag"

# ─── Document Processing ─────────────────────────────────────────────────────
EXTRACTED_IMAGES_DIR = os.path.join(os.path.dirname(__file__), "extracted_images")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ─── Retrieval ────────────────────────────────────────────────────────────────
RETRIEVAL_TOP_K = 5

# ─── Ensure directories exist ────────────────────────────────────────────────
os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
os.makedirs(EXTRACTED_IMAGES_DIR, exist_ok=True)
