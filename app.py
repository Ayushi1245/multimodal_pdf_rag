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
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* ── Background image with blur ── */
    .stApp {
        font-family: 'Outfit', sans-serif;
        background: transparent !important;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        background-image: url('https://i.pinimg.com/vwebp/1200x/33/79/93/33799327b6f6e6a9f264350e9484d302.webp');
        background-size: cover;
        background-position: center;
        filter: blur(3px) brightness(1.05);
        transform: scale(1.04);
        z-index: -1;
    }

    .stApp::after {
        content: "";
        position: fixed;
        inset: 0;
        background: rgba(255, 220, 235, 0.2);
        z-index: -1;
    }

    /* ── Hide default Streamlit chrome ── */
    [data-testid="stHeader"]        { visibility: hidden; }
    [data-testid="stToolbar"]       { visibility: hidden; }
    [data-testid="stAppDeployButton"] { display: none; }

    /* ── Markdown text colour ── */
    .stMarkdown p, .stMarkdown li { color: #C2E5F7 !important; }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.35) !important;
        backdrop-filter: blur(22px) !important;
        -webkit-backdrop-filter: blur(22px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.6) !important;
        box-shadow: 4px 0 24px rgba(255, 120, 180, 0.08);
    }

    .sidebar-header {
        font-size: 10px;
        font-weight: 700;
        color: #C2E5F7;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin: 1.2rem 0 0.5rem;
    }

    /* ── Buttons ── */
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #ff80ab, #f06292) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 16px rgba(255, 100, 150, 0.35) !important;
        transition: all 0.2s !important;
        font-family: 'Outfit', sans-serif !important;
    }

    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 22px rgba(255, 100, 150, 0.5) !important;
        opacity: 0.93 !important;
    }

    div[data-testid="stButton"] button * { color: white !important; }

    /* ── Delete button (sidebar col 2) — small red pill ── */
    section[data-testid="stSidebar"] div[data-testid="column"]:nth-child(2) div[data-testid="stButton"] button {
        background: rgba(255, 200, 210, 0.6) !important;
        border: 1px solid rgba(220, 80, 100, 0.35) !important;
        box-shadow: none !important;
        color: #C2E5F7 !important;
        border-radius: 6px !important;
        padding: 2px 7px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="column"]:nth-child(2) div[data-testid="stButton"] button:hover {
        background: rgba(220, 80, 100, 0.2) !important;
        transform: none !important;
        box-shadow: none !important;
    }

    section[data-testid="stSidebar"] div[data-testid="column"]:nth-child(2) div[data-testid="stButton"] button * {
        color: #C2E5F7 !important;
    }

    /* ── Clear Index button ── */
    section[data-testid="stSidebar"] div[data-testid="stButton"]:last-of-type button {
        background: rgba(255, 210, 220, 0.55) !important;
        border: 1px solid rgba(220, 80, 100, 0.3) !important;
        box-shadow: none !important;
        color: #C2E5F7 !important;
    }

    /* ── File Uploader ── */
    div[data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(12px);
        border: 1.5px dashed rgba(255, 128, 171, 0.55) !important;
        border-radius: 14px !important;
        padding: 1rem !important;
        transition: all 0.2s;
    }

    div[data-testid="stFileUploader"] *,
    div[data-testid="stFileUploader"] section {
        color: #C2E5F7 !important;
    }

    div[data-testid="stFileUploader"] section,
    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] {
        background: rgba(255, 255, 255, 0.75) !important;
        background-color: rgba(255, 255, 255, 0.75) !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 12px !important;
    }

    /* Make Upload button inside file uploader subtle/light */
    div[data-testid="stFileUploader"] button {
        background: white !important;
        color: #C2E5F7 !important;
        border: 1px solid #ddd !important;
        box-shadow: none !important;
        font-weight: 500 !important;
    }

    div[data-testid="stFileUploader"] button * {
        color: #C2E5F7 !important;
    }

    div[data-testid="stFileUploader"] button:hover {
        background: #f8f8f8 !important;
        border-color: #ccc !important;
        transform: none !important;
        box-shadow: none !important;
    }

    div[data-testid="stFileUploader"]:hover {
        border-color: #ff80ab !important;
        background: rgba(255, 255, 255, 0.6) !important;
    }

    /* ── Stat Cards ── */
    .stat-row {
        display: flex;
        gap: 14px;
        margin: 1.5rem 0;
    }

    .stat-card {
        flex: 1;
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 16px rgba(255, 120, 160, 0.08);
    }

    .stat-card:hover {
        background: rgba(255, 255, 255, 0.65);
        border-color: rgba(255, 128, 171, 0.5);
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(255, 120, 160, 0.18);
    }

    .stat-card .stat-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #C2E5F7;
        line-height: 1;
    }

    .stat-card .stat-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #C2E5F7;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 5px;
    }

    /* ── Indexed doc items ── */
    .indexed-doc {
        background: rgba(255, 255, 255, 0.5);
        border: 1px solid rgba(255, 180, 200, 0.5);
        border-radius: 10px;
        padding: 0.6rem 0.9rem;
        margin: 0.3rem 0;
        font-size: 0.88rem;
        color: #C2E5F7;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        transition: background 0.2s;
    }

    .indexed-doc:hover {
        background: rgba(255, 255, 255, 0.75);
        border-color: #ff80ab;
    }

    /* ── Header ── */
    .app-header {
        text-align: center;
        padding: 2.5rem 0 1.5rem;
    }

    .app-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        color: #C2E5F7;
        letter-spacing: -1px;
        margin-bottom: 0.4rem;
        text-shadow: 0 2px 12px rgba(255, 128, 171, 0.3);
    }

    .app-header p {
        color: #C2E5F7;
        font-size: 1.05rem;
        font-weight: 400;
    }

    /* ── Chat messages ── */
    .user-msg {
        background: rgba(255, 182, 193, 0.55);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 20px 20px 4px 20px;
        padding: 1rem 1.3rem;
        margin: 0.8rem 0 0.8rem auto;
        max-width: 80%;
        color: #C2E5F7 !important;
        box-shadow: 0 4px 14px rgba(255, 120, 160, 0.12);
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .assistant-msg {
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 20px 20px 20px 4px;
        padding: 1rem 1.3rem;
        margin: 0.8rem auto 0.8rem 0;
        max-width: 85%;
        color: #C2E5F7 !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .user-msg p, .assistant-msg p { color: inherit !important; }

    /* ── Source cards ── */
    .source-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        border-left: 3px solid #ff80ab;
        border-radius: 8px;
        padding: 0.9rem;
        margin: 0.4rem 0;
        font-size: 0.88rem;
        color: #C2E5F7;
        transition: all 0.2s;
    }

    .source-card:hover {
        background: rgba(255, 255, 255, 0.85);
        box-shadow: 0 4px 12px rgba(255, 120, 160, 0.12);
    }

    .source-card .source-header {
        font-weight: 700;
        color: #C2E5F7;
        font-size: 0.8rem;
        margin-bottom: 0.4rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ── Chat input ── */
    div[data-testid="stBottomBlockContainer"],
    div[data-testid="stBottomBlockContainer"] *,
    .stAppBottomBlockContainer,
    .stAppBottomBlockContainer *,
    .stBottom,
    .stBottom * {
        background: transparent !important;
        background-color: transparent !important;
    }

    .stChatInput, div[data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.45) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1.5px solid rgba(255, 128, 171, 0.4) !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 24px rgba(255, 120, 160, 0.08) !important;
    }

    .stChatInput:focus-within, div[data-testid="stChatInput"]:focus-within {
     
    }

    .stChatInput textarea, div[data-testid="stChatInput"] textarea {
        color: #C2E5F7 !important;
        background: transparent !important;
        font-family: 'Outfit', sans-serif !important;
    }

    .stChatInput textarea::placeholder,
    div[data-testid="stChatInput"] textarea::placeholder {
        color: rgba(194, 229, 247, 0.5) !important;
    }

    .stChatInput svg, div[data-testid="stChatInput"] svg {
        fill: #ff80ab !important;
    }

    /* ── Divider ── */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 150, 180, 0.35), transparent);
        margin: 1.5rem 0;
    }

    /* ── Empty state ── */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(255, 255, 255, 0.35);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        margin-top: 1.5rem;
        box-shadow: 0 4px 24px rgba(255, 120, 160, 0.08);
    }

    .empty-state .icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }

    .empty-state p { color: #C2E5F7 !important; font-size: 1rem; line-height: 1.8; }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50%       { transform: translateY(-10px); }
    }

    /* ── Progress bar ── */
    .stProgress > div > div {
        background: linear-gradient(90deg, #ff80ab, #f06292) !important;
        border-radius: 8px !important;
    }

    /* ── Info / success / warning ── */
    div[data-testid="stAlert"] {
        background: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 180, 200, 0.4) !important;
        color: #C2E5F7 !important;
    }
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
    st.markdown('''
        <h2 style="
            background: linear-gradient(135deg, #ff80ab, #f06292);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 0;
            font-weight: 700;
        ">📄 Document Manager</h2>
    ''', unsafe_allow_html=True)
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
            col1, col2 = st.columns([0.65, 0.35])
            with col1:
                st.markdown(f'<div class="indexed-doc" style="margin:0;">📑 {source}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("❌", key=f"del_{source}", help="Delete this file"):
                    ingest.delete_file(source)
                    st.session_state.processed_files.discard(source)
                    st.rerun()
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
        <div class="icon">📄</div>
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
