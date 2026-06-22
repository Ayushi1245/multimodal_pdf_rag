import os
import json
import hashlib
import fitz  # PyMuPDF
from PIL import Image
import io
import uuid

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_core.stores import BaseStore

class LocalFileStore(BaseStore[str, bytes]):
    """Custom LocalFileStore to avoid LangChain import errors."""
    def __init__(self, root_path: str):
        self.root_path = root_path
        os.makedirs(root_path, exist_ok=True)
        
    def mget(self, keys: list[str]) -> list[bytes | None]:
        values = []
        for key in keys:
            path = os.path.join(self.root_path, key)
            if os.path.exists(path):
                with open(path, "rb") as f:
                    values.append(f.read())
            else:
                values.append(None)
        return values
        
    def mset(self, key_value_pairs: list[tuple[str, bytes]]) -> None:
        for key, value in key_value_pairs:
            path = os.path.join(self.root_path, key)
            with open(path, "wb") as f:
                f.write(value)
                
    def mdelete(self, keys: list[str]) -> None:
        for key in keys:
            path = os.path.join(self.root_path, key)
            if os.path.exists(path):
                os.remove(path)
                
    def yield_keys(self, prefix: str | None = None):
        for file in os.listdir(self.root_path):
            if not prefix or file.startswith(prefix):
                yield file
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config
from utils import resize_image_to_base64, describe_image_with_groq

CACHE_FILE = "ingested_files.json"
DOCSTORE_DIR = "docstore"

def get_md5(file_path: str) -> str:
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

class CustomRetriever:
    def __init__(self, vectorstore, byte_store):
        self.vectorstore = vectorstore
        self.byte_store = byte_store

def get_retriever():
    """Returns a custom retriever containing the vectorstore and byte_store."""
    # Ensure directories exist
    os.makedirs(config.CHROMA_PERSIST_DIR, exist_ok=True)
    os.makedirs(DOCSTORE_DIR, exist_ok=True)

    embeddings = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL
    )

    vectorstore = Chroma(
        collection_name="multimodal_docs",
        persist_directory=config.CHROMA_PERSIST_DIR,
        embedding_function=embeddings
    )
    
    store = LocalFileStore(DOCSTORE_DIR)
    
    retriever = CustomRetriever(vectorstore=vectorstore, byte_store=store)
    
    return retriever

def ingest_pdf(file_path: str, progress_callback=None) -> tuple[int, int]:
    """
    Ingests a PDF by extracting text and images using PyMuPDF.
    Uses Gemini to summarize images.
    Returns (num_text_chunks, num_images).
    """
    file_name = os.path.basename(file_path)
    file_md5 = get_md5(file_path)
    
    # Check cache
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
    else:
        cache = {}
        
    if cache.get(file_name) == file_md5:
        print(f"Skipping {file_name} - already ingested.")
        return 0, 0
        
    retriever = get_retriever()
    doc_pdf = fitz.open(file_path)
    
    text_chunks = []
    image_docs = []
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    
    num_pages = len(doc_pdf)
    for i, page in enumerate(doc_pdf):
        if progress_callback:
            progress_callback(i, num_pages, f"Processing page {i+1}/{num_pages}...")
            
        # 1. Extract Text
        text = page.get_text()
        if text.strip():
            page_chunks = text_splitter.split_text(text)
            for chunk in page_chunks:
                doc_id = str(uuid.uuid4())
                summary_doc = Document(
                    page_content=chunk,
                    metadata={"doc_id": doc_id, "source": file_name, "page": i+1, "type": "text"}
                )
                text_chunks.append((doc_id, chunk, summary_doc))
                
        # 2. Extract Images
        images = page.get_images(full=True)
        for img_idx, img in enumerate(images):
            xref = img[0]
            base_image = doc_pdf.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Load into PIL
            try:
                pil_image = Image.open(io.BytesIO(image_bytes))
                # Skip tiny images (logos, bullets)
                if pil_image.width < 100 or pil_image.height < 100:
                    continue
                    
                b64_image = resize_image_to_base64(pil_image)
                
                # Describe image using Groq Vision
                if progress_callback:
                    progress_callback(i, num_pages, f"Summarizing image {img_idx+1} on page {i+1}...")
                summary = describe_image_with_groq(b64_image)
                
                doc_id = str(uuid.uuid4())
                summary_doc = Document(
                    page_content=summary,
                    metadata={"doc_id": doc_id, "source": file_name, "page": i+1, "type": "image"}
                )
                
                # Store full base64 in the docstore so we can retrieve it later
                image_docs.append((doc_id, b64_image, summary_doc))
                
            except Exception as e:
                print(f"Error processing image on page {i+1}: {e}")
                
    doc_pdf.close()
    
    # Save to MultiVectorRetriever
    if text_chunks or image_docs:
        if progress_callback:
            progress_callback(num_pages, num_pages, "Indexing in Chroma...")
            
        all_summary_docs = [item[2] for item in text_chunks] + [item[2] for item in image_docs]
        retriever.vectorstore.add_documents(all_summary_docs)
        
        # Add raw text and base64 images to local byte store
        kv_pairs = []
        for doc_id, raw_text, _ in text_chunks:
            kv_pairs.append((doc_id, raw_text.encode('utf-8')))
        for doc_id, b64_image, _ in image_docs:
            kv_pairs.append((doc_id, b64_image.encode('utf-8')))
            
        retriever.byte_store.mset(kv_pairs)
        
    # Update cache
    cache[file_name] = file_md5
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)
        
    return len(text_chunks), len(image_docs)

def delete_file(file_name: str) -> bool:
    """
    Deletes a specific file from the vectorstore, byte_store, and cache.
    """
    retriever = get_retriever()
    
    try:
        # 1. Get metadatas to find doc_ids for the byte_store
        results = retriever.vectorstore._collection.get(where={"source": file_name})
        if results and results.get("metadatas"):
            doc_ids = [m.get("doc_id") for m in results["metadatas"] if m.get("doc_id")]
            if doc_ids:
                retriever.byte_store.mdelete(doc_ids)
                
        # 2. Delete from Chroma vectorstore
        retriever.vectorstore._collection.delete(where={"source": file_name})
    except Exception as e:
        print(f"Error deleting {file_name} from vectorstore: {e}")
        return False
        
    # 3. Remove from cache
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cache = json.load(f)
            if file_name in cache:
                del cache[file_name]
                with open(CACHE_FILE, "w") as f:
                    json.dump(cache, f)
        except Exception as e:
            print(f"Error updating cache: {e}")
            return False
            
    return True

