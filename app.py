"""
Streamlit UI for the Multimodal RAG application.
Premium dark-themed interface for PDF upload, processing, and Q&A.
"""

import os
import json
import tempfile
import streamlit as st
import shutil
import base64

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

# ─── Base64 Image Helper ─────────────────────────────────────────────────────
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

bg_image_path = "/Users/ayushi/.gemini/antigravity-ide/brain/e9748397-6aa1-4274-a247-66e2f9754138/mountain_sunset_1784216741389.png"
bg_b64 = get_base64_image(bg_image_path)
bg_css = f"background-image: url('data:image/png;base64,{bg_b64}');" if bg_b64 else "background-color: #0b0d17;"

crystal_image_path = "/Users/ayushi/.gemini/antigravity-ide/brain/e9748397-6aa1-4274-a247-66e2f9754138/crystal_ball_1784216774102.png"
crystal_b64 = get_base64_image(crystal_image_path)
crystal_img_tag = f'<img src="data:image/png;base64,{crystal_b64}" alt="Crystal Ball" style="width: 80px; height: 80px; margin-bottom: 15px; object-fit: contain; filter: drop-shadow(0 0 15px rgba(167,139,250,0.5));" />' if crystal_b64 else '🔮'

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown(
    f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ── Background image with blur ── */
    .stApp {{
        font-family: 'Inter', sans-serif;
        background: transparent !important;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        {bg_css}
        background-size: cover;
        background-position: top;
        opacity: 0.9;
        z-index: -2;
        pointer-events: none;
    }}

    .stApp::after {{
        content: "";
        position: fixed;
        inset: 0;
        background: linear-gradient(to bottom, rgba(11, 13, 23, 0.4), #0b0d17 60%);
        z-index: -1;
        pointer-events: none;
    }}

    /* ── Hide default Streamlit chrome ── */
    [data-testid="stHeader"]        {{ visibility: hidden; }}
    [data-testid="stToolbar"]       {{ visibility: hidden; }}
    [data-testid="stAppDeployButton"] {{ display: none; }}

    /* ── Markdown text colour ── */
    .stMarkdown p, .stMarkdown li {{ color: #cbd5e1 !important; font-weight: 400 !important; }}

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {{
        background: rgba(11, 13, 23, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(46, 50, 72, 0.5) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.2);
    }}

    .sidebar-header {{
        font-size: 11px;
        font-weight: 600;
        color: rgba(148, 163, 184, 0.8);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 1.2rem 0 0.5rem;
    }}

    /* ── Buttons ── */
    div[data-testid="stButton"] button {{
        background: #8b5cf6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2) !important;
        transition: all 0.2s !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.5rem 1rem !important;
    }}

    div[data-testid="stButton"] button:hover {{
        background: #7c3aed !important;
        box-shadow: 0 6px 16px rgba(139, 92, 246, 0.3) !important;
        transform: translateY(-1px) !important;
    }}

    div[data-testid="stButton"] button * {{ color: white !important; }}

    /* ── Delete button (sidebar col 2) — small icon ── */
    section[data-testid="stSidebar"] div[data-testid="column"]:nth-child(2) div[data-testid="stButton"] button {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: rgba(239, 68, 68, 0.8) !important;
        padding: 2px 5px !important;
        font-size: 14px !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="column"]:nth-child(2) div[data-testid="stButton"] button:hover {{
        background: transparent !important;
        color: #ef4444 !important;
        transform: none !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="column"]:nth-child(2) div[data-testid="stButton"] button * {{
        color: rgba(239, 68, 68, 0.8) !important;
    }}

    /* ── Clear Index button ── */
    section[data-testid="stSidebar"] div[data-testid="stButton"]:last-of-type button {{
        background: transparent !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        box-shadow: none !important;
        color: #a78bfa !important;
    }}
    
    section[data-testid="stSidebar"] div[data-testid="stButton"]:last-of-type button:hover {{
        background: rgba(139, 92, 246, 0.1) !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stButton"]:last-of-type button * {{
        color: #a78bfa !important;
    }}

    /* ── File Uploader ── */
    div[data-testid="stFileUploader"] {{
        background: #171a26 !important;
        border: 1px dashed rgba(139, 92, 246, 0.4) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        transition: all 0.2s;
        text-align: center;
    }}

    div[data-testid="stFileUploader"] *,
    div[data-testid="stFileUploader"] section {{
        color: #94a3b8 !important;
    }}

    div[data-testid="stFileUploader"] section,
    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
    }}

    /* Make Upload button inside file uploader solid purple */
    div[data-testid="stFileUploader"] button {{
        background: rgba(139, 92, 246, 0.1) !important;
        color: #a78bfa !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        font-weight: 500 !important;
        box-shadow: none !important;
        border-radius: 8px !important;
        margin-top: 10px !important;
    }}

    div[data-testid="stFileUploader"] button * {{
        color: #a78bfa !important;
    }}

    div[data-testid="stFileUploader"] button:hover {{
        background: rgba(139, 92, 246, 0.2) !important;
        border-color: rgba(139, 92, 246, 0.5) !important;
    }}

    div[data-testid="stFileUploader"]:hover {{
        border-color: rgba(139, 92, 246, 0.8) !important;
    }}

    /* ── Stat Cards ── */
    .stat-row {{
        display: flex;
        gap: 24px;
        margin: 2rem 0;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }}

    .stat-card {{
        flex: 1;
        background: rgba(19, 21, 31, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(46, 50, 72, 0.5);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.25s ease;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 140px;
    }}
    
    /* Highlight the middle stat card */
    .stat-card:nth-child(2) {{
        border: 1px solid rgba(139, 92, 246, 0.5);
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.15);
    }}

    .stat-card:hover {{
        border-color: rgba(139, 92, 246, 0.6);
        transform: translateY(-2px);
        background: rgba(19, 21, 31, 0.85);
    }}

    .stat-card .stat-value {{
        font-size: 2.5rem;
        font-weight: 700;
        color: #f8fafc;
        line-height: 1;
        margin-bottom: 8px;
    }}

    .stat-card .stat-label {{
        font-size: 11px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* ── Indexed doc items ── */
    .indexed-doc {{
        background: rgba(30, 34, 53, 0.6);
        border: 1px solid rgba(46, 50, 72, 0.5);
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.3rem 0;
        font-size: 14px;
        color: #e2e8f0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        transition: background 0.2s;
    }}
    
    .indexed-doc:hover {{
        background: rgba(30, 34, 53, 0.9);
        border-color: rgba(139, 92, 246, 0.4);
    }}

    /* ── Header ── */
    .app-header {{
        text-align: center;
        padding: 3rem 0 1rem;
    }}

    .app-header h1 {{
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }}
    
    .app-header h1 span {{
        color: #a78bfa;
    }}

    .app-header p {{
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 400;
        line-height: 1.6;
    }}

    /* ── Chat messages ── */
    .user-msg {{
        background: rgba(139, 92, 246, 0.15);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 12px 12px 2px 12px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0 1rem auto;
        max-width: 80%;
        color: #f8fafc !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
        font-size: 1rem;
        line-height: 1.6;
    }}

    .assistant-msg {{
        background: rgba(30, 34, 53, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(46, 50, 72, 0.5);
        border-radius: 12px 12px 12px 2px;
        padding: 1.2rem 1.5rem;
        margin: 1rem auto 1rem 0;
        max-width: 85%;
        color: #f8fafc !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
        font-size: 1rem;
        line-height: 1.6;
    }}

    .user-msg p, .assistant-msg p {{ color: inherit !important; }}

    /* ── Source cards ── */
    .source-card {{
        background: rgba(19, 21, 31, 0.6);
        border-left: 3px solid #8b5cf6;
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #cbd5e1;
    }}

    .source-card .source-header {{
        font-weight: 600;
        color: #f8fafc;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* ── Chat input ── */
    div[data-testid="stBottomBlockContainer"],
    div[data-testid="stBottomBlockContainer"] *,
    .stAppBottomBlockContainer,
    .stAppBottomBlockContainer *,
    .stBottom,
    .stBottom * {{
        background: transparent !important;
        background-color: transparent !important;
    }}
    
    .stChatInput, div[data-testid="stChatInput"] {{
        background: rgba(19, 21, 31, 0.8) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(46, 50, 72, 0.6) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        max-width: 800px !important;
        margin: 0 auto !important;
    }}
    
    .stChatInput:focus-within, div[data-testid="stChatInput"]:focus-within {{
        border-color: rgba(139, 92, 246, 0.5) !important;
    }}

    .stChatInput textarea, div[data-testid="stChatInput"] textarea {{
        color: #f8fafc !important;
        background: transparent !important;
        font-family: 'Inter', sans-serif !important;
    }}

    .stChatInput textarea::placeholder,
    div[data-testid="stChatInput"] textarea::placeholder {{
        color: #64748b !important;
    }}

    .stChatInput svg, div[data-testid="stChatInput"] svg {{
        fill: #8b5cf6 !important;
    }}

    /* ── Divider ── */
    .divider {{
        height: 1px;
        background: rgba(46, 50, 72, 0.5);
        margin: 1.5rem 0;
    }}

    /* ── Empty state ── */
    .empty-state {{
        text-align: center;
        padding: 5rem 2rem;
        background: rgba(30, 34, 53, 0.4);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(46, 50, 72, 0.5);
        border-radius: 20px;
        margin-top: 2rem;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }}

    .empty-state .icon {{
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        color: #94a3b8;
    }}

    .empty-state p {{ color: #94a3b8 !important; font-size: 1rem; line-height: 1.8; }}

    /* ── Progress bar ── */
    .stProgress > div > div {{
        background: #8b5cf6 !important;
        border-radius: 8px !important;
    }}

    /* ── Info / success / warning ── */
    div[data-testid="stAlert"] {{
        background: rgba(30, 34, 53, 0.8) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(46, 50, 72, 0.5) !important;
        color: #e2e8f0 !important;
    }}
    
    div[data-testid="stAlert"] * {{
        color: #e2e8f0 !important;
    }}
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
        <div class="stat-card active-card">
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

            t, i = ingest.ingest_pdf(tmp_path, original_file_name=file_name, progress_callback=progress_cb)
            
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
            background: linear-gradient(135deg, #1886B9, #1886B9);
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
    f"""
<div class="app-header">
    {crystal_img_tag}
    <h1>Multimodal <span>RAG</span></h1>
    <p>Upload PDFs with text, images & charts — ask anything.</p>
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
