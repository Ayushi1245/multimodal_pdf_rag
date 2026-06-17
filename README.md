# multimodal_pdf_rag
# 🔮 Multimodal PDF RAG

> Chat with your PDF documents — including the **images, charts, and diagrams** inside them.

Most RAG systems only read text. This one reads everything.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6B35?style=for-the-badge&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)

---

## 🚀 What It Does

Upload any PDF and ask questions about it — including questions about charts, graphs, tables, and figures that traditional RAG systems completely miss.

- **Extracts text and images** from PDFs simultaneously using PyMuPDF
- **Summarizes images** using Groq's vision model so they become text-searchable
- **Shows visual citations** — when the answer references an image, it displays that image inline in the chat
- **Runs locally** — embeddings and vector storage are fully local, no extra API costs

---

## 🧠 Architecture

```
PDF Upload
    │
    ▼
┌─────────────────────────────────────────┐
│              ingest.py                  │
│  ┌─────────────┐    ┌────────────────┐  │
│  │  Text Chunks│    │  Image Extract │  │
│  │ (LangChain  │    │  (PyMuPDF)     │  │
│  │  Splitter)  │    │       │        │  │
│  └──────┬──────┘    │  Groq Vision   │  │
│         │           │  (summarize)   │  │
│         └─────┬─────┘       │        │  │
│               ▼             ▼        │  │
│         Embeddings (all-MiniLM-L6-v2)│  │
│               │                      │  │
│         ChromaDB + LocalFileStore    │  │
└─────────────────────────────────────────┘
    │
    ▼
User Query
    │
    ▼
┌─────────────────────────────────────────┐
│             rag_chain.py                │
│  Similarity Search → Top 6 Chunks      │
│  Build Prompt (text + base64 images)   │
│  Groq llama-3.3-70b-versatile          │
└─────────────────────────────────────────┘
    │
    ▼
Answer + Visual Citations in Streamlit UI
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (dark theme, glassmorphism UI) |
| PDF Parsing | PyMuPDF (`fitz`) |
| Text Chunking | LangChain `RecursiveCharacterTextSplitter` |
| Image Summarization | Groq `llama-3.2-11b-vision-preview` |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | ChromaDB (local) |
| Chat Model | Groq `llama-3.3-70b-versatile` |
| Image Storage | LangChain `LocalFileStore` |

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Ayushi1245/multimodal_pdf_rag.git
cd multimodal_pdf_rag
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```
Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 4. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
multimodal_pdf_rag/
├── app.py           # Streamlit frontend & chat UI
├── ingest.py        # PDF parsing, image extraction, embedding
├── rag_chain.py     # Retrieval logic & LLM prompt construction
├── config.py        # Model config & environment variables
├── requirements.txt
└── .env             # API keys (not committed)
```

---

## 💡 Why Multimodal RAG?

Standard RAG pipelines skip images entirely. For documents like:
- Research papers with figures and graphs
- Financial reports with charts
- Technical manuals with diagrams
- Medical reports with scans

...text-only RAG gives incomplete answers. This system ingests the full document — text and visuals — so nothing is missed.

---

## 📬 Contact

Built by [Ayushi](https://github.com/Ayushi1245) · Open for freelance AI/ML projects
[ayushi7607053@gmail.com](mailto:ayushi7607053@gmail.com) · [LinkedIn](https://linkedin.com/in/ayushi1245)
