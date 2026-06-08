"""
RAG Chain module for the Multimodal RAG application using Google Gemini.
"""

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import ingest
import config

# System prompt for the RAG answer generation
SYSTEM_PROMPT = """You are a knowledgeable assistant that answers questions based on the provided context from PDF documents.

Instructions:
- Answer the question using ONLY the provided context (text excerpts and image descriptions).
- If the context contains relevant information from images, charts, or diagrams, incorporate that data into your answer.
- Cite your sources by mentioning the document name and page number when available.
- If the context does not contain enough information to answer the question, say so clearly.
- Be thorough but concise. Use bullet points or structured formatting when it improves clarity.
- If data from charts or tables is referenced, include specific numbers and labels."""


def ask_question(query: str) -> dict:
    """
    Answer a question using the Gemini multimodal RAG pipeline.
    """
    retriever = ingest.get_retriever()
    
    # 1. Get documents from vectorstore
    docs = retriever.vectorstore.similarity_search(query, k=6)
    
    if not docs:
        return {
            "answer": "I don't have any documents indexed yet. Please upload and process some PDF files first.",
            "sources": [],
            "image_refs": [],
        }

    # 2. Fetch raw data from byte store using doc_ids
    doc_ids = [doc.metadata["doc_id"] for doc in docs]
    raw_data = retriever.byte_store.mget(doc_ids)
    
    text_parts = []
    image_refs = []
    user_content = [{"type": "text", "text": f"SYSTEM PROMPT:\n{SYSTEM_PROMPT}\n\nContext from documents:\n\n"}]

    for i, (doc, raw_bytes) in enumerate(zip(docs, raw_data), 1):
        if not raw_bytes:
            continue
            
        source = doc.metadata.get("source", "Unknown")
        page_num = doc.metadata.get("page", "?")
        doc_type = doc.metadata.get("type", "text")

        if doc_type == "image":
            # raw_bytes contains the base64 encoded image
            b64_image = raw_bytes.decode('utf-8')
            
            # Add description to context
            text_context = f"[Source {i}: {source}, Page {page_num} — Image Description]\n{doc.page_content}\n\n"
            user_content[0]["text"] += text_context
            
            # Add image to prompt
            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}
            })
            
            image_refs.append({
                "b64": b64_image,
                "page": page_num,
                "source": source
            })
        else:
            # raw_bytes contains the raw text chunk
            text_chunk = raw_bytes.decode('utf-8')
            text_context = f"[Source {i}: {source}, Page {page_num} — Text Chunk]\n{text_chunk}\n\n"
            user_content[0]["text"] += text_context
            text_parts.append(text_context)

    # 3. Add Question
    user_content[0]["text"] += f"---\n\nQuestion: {query}"

    # 4. Call Groq
    model = ChatGroq(
        model=config.ANSWER_MODEL,
        api_key=config.GROQ_API_KEY,
        max_tokens=2048,
        temperature=0.3,
    )

    try:
        msg = model.invoke([HumanMessage(content=user_content)])
        answer = msg.content
    except Exception as e:
        answer = f"Error generating answer: {str(e)}"

    return {
        "answer": answer,
        "sources": docs,
        "image_refs": image_refs,
    }
