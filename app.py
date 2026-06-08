"""
Streamlit UI for the Multimodal RAG application.
Premium dark-themed interface for PDF upload, processing, and Q&A.
"""

import os
import json
import tempfile
import streamlit as st
import shutil

import config
import ingest
import rag_chain


# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multimodal RAG · Document Intelligence",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global ─────────────────────────────────────────── */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ── Header ─────────────────────────────────────────── */
    .app-header {
        text-align: center;
        padding: 2rem 0 1rem;
    }
    .app-header h1 {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a78bfa, #818cf8, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    .app-header p {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 300;
    }

    /* ── Stat Cards ─────────────────────────────────────── */
    .stat-row {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    .stat-card {
        flex: 1;
        background: linear-gradient(135deg, rgba(99,102,241,0.10), rgba(139,92,246,0.08));
        border: 1px solid rgba(139,92,246,0.18);
        border-radius: 14px;
        padding: 1.1rem 1.25rem;
        text-align: center;
    }
    .stat-card .stat-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #a78bfa;
    }
    .stat-card .stat-label {
        font-size: 0.78rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 0.2rem;
    }

    /* ── Chat Messages ──────────────────────────────────── */
    .user-msg {
        background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.10));
        border: 1px solid rgba(139,92,246,0.2);
        border-radius: 16px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
    }
    .assistant-msg {
        background: rgba(30, 32, 48, 0.6);
        border: 1px solid rgba(148,163,184,0.1);
        border-radius: 16px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
    }

    /* ── Source Cards ────────────────────────────────────── */
    .source-card {
        background: rgba(15, 17, 28, 0.7);
        border: 1px solid rgba(139,92,246,0.12);
        border-radius: 12px;
        padding: 0.85rem 1rem;
        margin: 0.4rem 0;
        font-size: 0.88rem;
        color: #cbd5e1;
    }
    .source-card .source-header {
        font-weight: 600;
        color: #a78bfa;
        font-size: 0.8rem;
        margin-bottom: 0.35rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* ── Sidebar ────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(139,92,246,0.12);
    }
    .sidebar-header {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin: 1.5rem 0 0.5rem;
    }
    .indexed-doc {
        background: rgba(99,102,241,0.08);
        border: 1px solid rgba(139,92,246,0.12);
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        margin: 0.3rem 0;
        font-size: 0.85rem;
        color: #c4b5fd;
    }

    /* ── Image Thumbnails ───────────────────────────────── */
    .image-grid {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        margin-top: 0.5rem;
    }
    .image-thumb {
        border: 1px solid rgba(139,92,246,0.2);
        border-radius: 10px;
        overflow: hidden;
        max-width: 200px;
    }
    .image-thumb img {
        width: 100%;
        display: block;
    }
    .image-caption {
        font-size: 0.72rem;
        color: #94a3b8;
        padding: 0.3rem 0.5rem;
        text-align: center;
        background: rgba(15, 17, 28, 0.8);
    }

    /* ── Misc ───────────────────────────────────────────── */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139,92,246,0.3), transparent);
        margin: 1.5rem 0;
    }
    .empty-state {
        text-align: center;
        color: #64748b;
        padding: 3rem 1rem;
    }
    .empty-state .icon {
        font-size: 3rem;
        margin-bottom: 0.75rem;
    }
    .empty-state p {
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)


# ─── Session State Initialization ────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()


# ─── Helper Functions ────────────────────────────────────────────────────────
def get_indexed_sources():
    if os.path.exists(ingest.CACHE_FILE):
        try:
            with open(ingest.CACHE_FILE) as f:
                return list(json.load(f).keys())
        except Exception:
            pass
    return []

def _render_stat_cards():
    """Render the statistics cards row."""
    try:
        retriever = ingest.get_retriever()
        doc_count = retriever.vectorstore._collection.count()
        sources = get_indexed_sources()
        source_count = len(sources)
    except Exception:
        doc_count = 0
        source_count = 0

    st.markdown(
        f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-value">{source_count}</div>
            <div class="stat-label">Documents</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{doc_count}</div>
            <div class="stat-label">Indexed Chunks</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(st.session_state.chat_history) // 2}</div>
            <div class="stat-label">Questions Asked</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def _process_uploaded_files(uploaded_files):
    """Process uploaded PDF files."""
    st.session_state.processing = True

    total_text = 0
    total_img = 0
    indexed = get_indexed_sources()

    for file_idx, uploaded_file in enumerate(uploaded_files):
        file_name = uploaded_file.name

        # Check for duplicates
        if file_name in indexed:
            st.sidebar.info(f"⏭️ '{file_name}' already indexed — skipping.")
            continue

        st.sidebar.markdown(f"**Processing:** `{file_name}`")

        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            progress_bar = st.sidebar.progress(0, text="Extracting...")
            
            def progress_cb(curr, tot, text):
                pct = int((curr / tot) * 100) if tot > 0 else 100
                progress_bar.progress(pct, text=text)

            t, i = ingest.ingest_pdf(tmp_path, progress_callback=progress_cb)
            
            total_text += t
            total_img += i

            progress_bar.progress(100, text=f"✅ Done — {t} text + {i} image chunks")
            st.session_state.processed_files.add(file_name)

        except Exception as e:
            st.sidebar.error(f"❌ Error processing '{file_name}': {str(e)}")

        finally:
            # Clean up temp file
            os.unlink(tmp_path)

    st.session_state.processing = False

    if total_text or total_img:
        st.sidebar.success(
            f"🎉 Indexed **{total_text}** text chunks and "
            f"**{total_img}** image summaries!"
        )

    return total_text, total_img


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📄 Document Manager")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # File uploader
    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        key="pdf_uploader",
        help="Upload one or more PDF files to process and index.",
    )

    # Process button
    if uploaded_files:
        if st.button(
            "⚡ Process Documents",
            use_container_width=True,
            disabled=st.session_state.processing,
            type="primary",
        ):
            text_docs, img_docs = _process_uploaded_files(uploaded_files)
            if text_docs or img_docs:
                st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Indexed documents list
    st.markdown('<div class="sidebar-header">📚 Indexed Documents</div>', unsafe_allow_html=True)

    indexed_sources = get_indexed_sources()

    if indexed_sources:
        for source in indexed_sources:
            st.markdown(f'<div class="indexed-doc">📑 {source}</div>', unsafe_allow_html=True)
    else:
        st.caption("No documents indexed yet.")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Clear index button
    if indexed_sources:
        if st.button("🗑️ Clear Index", use_container_width=True):
            if os.path.exists(config.CHROMA_PERSIST_DIR):
                shutil.rmtree(config.CHROMA_PERSIST_DIR)
            if os.path.exists(ingest.DOCSTORE_DIR):
                shutil.rmtree(ingest.DOCSTORE_DIR)
            if os.path.exists(ingest.CACHE_FILE):
                os.remove(ingest.CACHE_FILE)
                
            st.session_state.chat_history = []
            st.session_state.processed_files = set()
            st.success("Index cleared!")
            st.rerun()

    # API Key status
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    if config.GROQ_API_KEY and config.GROQ_API_KEY != "your-groq-api-key-here":
        st.markdown("🟢 **API Key:** Connected")
    else:
        st.markdown("🔴 **API Key:** Not configured")
        st.caption("Create a `.env` file with `GROQ_API_KEY=gsk_...`")


# ─── Main Area ───────────────────────────────────────────────────────────────

# Header
st.markdown(
    """
<div class="app-header">
    <h1>🔮 Multimodal RAG</h1>
    <p>Upload PDFs with text, images & charts — ask anything. Powered by Groq.</p>
</div>
""",
    unsafe_allow_html=True,
)

# Stats
_render_stat_cards()

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Chat history display
if not st.session_state.chat_history:
    st.markdown(
        """
    <div class="empty-state">
        <div class="icon">📚</div>
        <p>
            <strong>Upload a PDF</strong> in the sidebar to get started.<br>
            Once processed, ask any question about your documents —<br>
            text, tables, charts, and images are all searchable.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
else:
    for entry in st.session_state.chat_history:
        role = entry["role"]

        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(entry["content"])
        else:
            with st.chat_message("assistant", avatar="🔮"):
                st.markdown(entry["content"])

                # Show source documents
                if "sources" in entry and entry["sources"]:
                    with st.expander(f"📎 Sources ({len(entry['sources'])} references)", expanded=False):
                        for src in entry["sources"]:
                            src_type = src.metadata.get("type", "text")
                            source_name = src.metadata.get("source", "Unknown")
                            page = src.metadata.get("page", "?")

                            if src_type == "image":
                                st.markdown(
                                    f'<div class="source-card">'
                                    f'<div class="source-header">🖼️ {source_name} · Page {page}</div>'
                                    f"{src.page_content[:300]}..."
                                    f"</div>",
                                    unsafe_allow_html=True,
                                )
                            else:
                                st.markdown(
                                    f'<div class="source-card">'
                                    f'<div class="source-header">📝 {source_name} · Page {page}</div>'
                                    f"{src.page_content[:300]}..."
                                    f"</div>",
                                    unsafe_allow_html=True,
                                )

                # Show referenced images
                if "image_refs" in entry and entry["image_refs"]:
                    with st.expander(f"🖼️ Referenced Images ({len(entry['image_refs'])})", expanded=False):
                        cols = st.columns(min(len(entry["image_refs"]), 3))
                        for idx, ref in enumerate(entry["image_refs"]):
                            with cols[idx % 3]:
                                try:
                                    b64_data = ref["b64"]
                                    st.image(
                                        f"data:image/jpeg;base64,{b64_data}",
                                        caption=f"{ref['source']} — Page {ref['page']}",
                                        use_container_width=True,
                                    )
                                except Exception:
                                    st.caption(f"⚠️ Image unavailable: Page {ref['page']}")


# ─── Chat Input ──────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a question about your documents...", key="chat_input"):
    indexed = get_indexed_sources()

    if len(indexed) == 0:
        st.warning("⚠️ No documents indexed yet. Upload and process a PDF first.")
    else:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Generate answer
        with st.spinner("🔍 Searching documents and generating answer with Groq..."):
            result = rag_chain.ask_question(prompt)

        # Add assistant message with sources
        assistant_entry = {
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"],
            "image_refs": result["image_refs"],
        }
        st.session_state.chat_history.append(assistant_entry)

        st.rerun()
