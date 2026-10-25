
Claude finished the response
---
name: multimodal-pdf-rag
description: Expert at building and maintaining a Multimodal RAG system for PDFs containing text, tables, charts, and images using LangChain, Unstructured.io (hi_res), GPT-4o, Chroma, and Streamlit. Handles ingestion, image description, multi-vector retrieval, and multimodal answering.
version: 1.0
tags: [rag, multimodal, langchain, unstructured, gpt-4o, streamlit, pdf-parsing, vision]
---

# Multimodal PDF RAG Assistant Skill

You are an expert AI engineer specializing in **Multimodal Retrieval-Augmented Generation (RAG)** systems that can truly understand complex PDFs with text, tables, charts, and images.

## Project Overview
This project allows users to upload PDFs and chat with both textual and visual content using GPT-4o as the vision model. It extracts structured data (text + tables) and rich descriptions of images/charts, then uses a MultiVectorRetriever for accurate answers with source images.

**Core Tech Stack:**
- LangChain + LangChain Community
- Unstructured.io (hi_res strategy) for PDF parsing
- GPT-4o (for image description during ingestion and final multimodal generation)
- Chroma (vector store)
- MultiVectorRetriever pattern (summaries for retrieval + raw content + images for generation)
- Streamlit for the frontend

## When to Use This Skill
Use this skill when the user wants to:
- Improve PDF ingestion for complex documents (tables, charts, figures)
- Add or fix multimodal capabilities (image description + vision-based answering)
- Enhance the Streamlit UI for showing source images
- Optimize retrieval accuracy for visual-heavy queries
- Debug issues with table extraction or image handling

## Core Responsibilities

### 1. Ingestion Pipeline
- Use `partition_pdf` with `strategy="hi_res"` and `infer_table_structure=True`
- Separate NarrativeText, Title, Table, and Image elements
- For every image/chart: Generate detailed, quantitative descriptions using GPT-4o (include trends, numbers, labels)
- Store text/tables as Documents and image descriptions as separate Documents in Chroma
- Keep raw image paths in metadata for later retrieval

### 2. Retrieval Strategy
- Use `MultiVectorRetriever` with Chroma + LocalFileStore (or InMemoryStore)
- Retrieve both text chunks and image summary documents
- Return raw content + associated image paths

### 3. Generation
- Build multimodal messages for GPT-4o
- Include relevant text context + actual images (base64) when available
- Always cite sources and reference page numbers / figures when possible

### 4. UI/UX Guidelines
- Show relevant source images below the answer
- Support clear conversation history
- Display "Relevant Images from Document" section when visuals are used

## Best Practices
- Always describe images with context from surrounding text
- Limit number of images sent to GPT-4o in one call (usually 1–3)
- Use `text-embedding-3-large` for embeddings
- Keep image descriptions detailed and data-driven (avoid vague summaries)
- Handle errors gracefully when images fail to load

## Common Tasks You Should Help With
- Writing/improving `ingest.py`
- Fixing Streamlit chat interface (`app.py`)
- Enhancing the vision prompt for better chart/table understanding
- Adding support for multiple PDFs
- Implementing re-ranking or hybrid search
- Creating evaluation examples

You have access to the full project structure:
- `ingest.py`, `app.py`, `utils.py`
- `chroma_db/` folder
- `extracted_images/` folder

Always provide clean, well-commented, production-ready code. Prefer clarity and modularity.

Current date: April 2026. Use latest stable practices for LangChain multimodal RAG.
Show more
15:31
I can see you've shared a skill definition for a Multimodal PDF RAG system. How can I help you with this project?

Are you looking to:

Build the project from scratch (I can generate ingest.py, app.py, utils.py)
Fix or improve existing code you already have
Ask a specific question about the architecture or implementation
Just let me know what you need and I'll dive in!

i want to build this so change the skill.md file so that the multimodal pdf rag system is made very easily

15:32
The skill files in /mnt/skills/ are read-only, so I can't edit them directly. But I can build the entire Multimodal PDF RAG system for you right now — all the code files ready to run.

Let me check the skill file first, then generate everything.


Reading the skill definition
Reading the skill definition
Now let me build the full project:


Ran a command, created a file
Ran a command, created a file
Claude's response was interrupted.
which api key is used?

15:33
The system uses the OpenAI API key (for GPT-4o).

You need to set it in a .env file in the project root:

OPENAI_API_KEY=sk-...your-key-here...
It's used for two things:

During ingestion — GPT-4o Vision describes images/charts found in the PDF
During chat — GPT-4o answers questions using retrieved text + images
That's the only key needed. No other services require authentication since Chroma runs locally and Unstructured.io is used in its free, local mode.

how to get it?

15:33
Here's how to get your OpenAI API key:

Go to platform.openai.com
Sign up / Log in with your Google or email account
Click your profile icon (top right) → "API keys"
Click "Create new secret key" → give it a name → Copy it
Then paste it in your .env file:

OPENAI_API_KEY=sk-...your-key-here...
Important things to know:

The key is shown only once — copy it immediately
GPT-4o requires a paid account (add billing at platform.openai.com/settings/billing)
For this RAG project, costs are very low — roughly $0.01–0.05 per PDF page with images
why these rag projects take way too long to load?

15:38
Great question! Here are the main reasons RAG projects are slow:

1. 🐌 PDF Parsing (Biggest culprit)
unstructured with hi_res strategy runs OCR + layout detection on every page
It uses heavy ML models (detectron2, tesseract) locally
A 20-page PDF can take 2–5 minutes just to parse
2. 🧠 Embedding Generation
Every text chunk gets sent to OpenAI's embedding API
100 chunks = 100 API calls (or batched, but still slow)
text-embedding-3-large is accurate but heavier than small
3. 🖼️ Image Description via GPT-4o
Each image/chart is sent to GPT-4o Vision one by one
A PDF with 10 charts = 10 separate GPT-4o API calls during ingestion
4. 💾 Chroma Writes
Writing vectors to disk is slower than in-memory stores
How to Speed It Up
Fix	Speedup
Use strategy="fast" instead of hi_res	10x faster parsing
Cache ingestion results (skip re-processing)	Instant on reload
Use text-embedding-3-small	2x faster + cheaper
Batch image descriptions	Parallel API calls
Show a progress bar in Streamlit	Feels faster
The most impactful fix is caching — once a PDF is ingested, never re-process it. Want me to build that into the project?

Error processing 'Ayushi_nokia (3).pdf': Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}

16:19
This is a billing issue, not a code bug. Here's what's happening:

Why You're Getting 429
Your OpenAI account has no credits / free tier expired. GPT-4o is a paid model — it won't work without billing set up.

Fix It (2 minutes)
Go to platform.openai.com/settings/billing
Click "Add payment method"
Add your card
Click "Add credits" → start with $5 (enough for lots of testing)
Verify It Worked
Go to platform.openai.com/usage — you should see a credit balance.

Cheaper Alternative (if you don't want to pay)
You can swap GPT-4o for Google Gemini which has a free tier:

Model	Cost	Free Tier
GPT-4o	~$0.01/page	❌ No
Gemini 1.5 Flash	~$0.001/page	✅ Yes
Gemini 1.5 Pro	~$0.003/page	✅ Limited
Want me to rewrite the project to use Gemini instead so you can run it for free?

i want a free tier solution

16:20
I'll rewrite the entire project using Google Gemini (free tier) instead of GPT-4o. Let me set it up properly.


Created 4 files, ran 2 commands, viewed a file
Created 4 files, ran 2 commands, viewed a file
Claude's response was interrupted.
give me skill.md solution for this

16:22
The skill files in /mnt/skills/ are read-only, so I'll create a standalone SKILL.md file for your project instead:


Created a file, read a file
Created a file, read a file
Here's your complete SKILL.md along with all project files. Here's a quick summary of what's inside:

SKILL.md covers:

Full project structure with folder layout
Step-by-step setup (API key → install → run)
How ingestion and retrieval work (with flow diagrams)
Key design decisions and why each was made
Gemini free tier limits (15 req/min — plenty for personal use)
Common fixes for errors like 429, missing images, slow loading
Tips for improving retrieval accuracy and image descriptions
To run the project:

bash
# 1. Install
pip install -r requirements.txt

# 2. Create .env
echo "GOOGLE_API_KEY=your-key-here" > .env

# 3. Launch
streamlit run app.py
Get your free key at aistudio.google.com → Sign in → Get API key.


SKILL.md
Skill 

App
PY 

Ingest
PY 

Utils
PY 

Requirements
TXT 





Claude is AI and can make mistakes. Please double-check responses.


normal
SKILL.md
Multimodal PDF RAG — Skill Guide (Gemini Free Tier)
Project Overview
A Multimodal RAG system that lets users upload PDFs and chat with text, tables, charts, and images — completely free using Google Gemini 1.5 Flash.

Tech Stack:

PyMuPDF (fitz) — Fast PDF parsing (text + image extraction)
Gemini 1.5 Flash — Free image description + multimodal answering
models/embedding-001 — Free Gemini embeddings
Chroma — Local vector store (no cost)
MultiVectorRetriever — Retrieves both text and image docs
Streamlit — Chat UI
LocalFileStore — Persistent docstore
Project Structure
multimodal-pdf-rag/
├── app.py                  # Streamlit chat UI
├── ingest.py               # PDF ingestion pipeline
├── utils.py                # Gemini helpers (image description, encoding)
├── requirements.txt        # All dependencies
├── .env                    # GOOGLE_API_KEY=your-key-here
├── .env.example            # Template for .env
├── ingested_files.json     # Cache — avoids re-processing same PDF
├── chroma_db/              # Chroma vector store (auto-created)
├── extracted_images/       # Images extracted from PDFs (auto-created)
└── docstore/               # LangChain LocalFileStore (auto-created)
Setup (One Time)
1. Get Free Gemini API Key
Go to aistudio.google.com
Sign in with Google
Click Get API key → Copy it
2. Install Dependencies
bash
pip install -r requirements.txt
3. Set API Key
Create a .env file:

GOOGLE_API_KEY=your-gemini-api-key-here
4. Run the App
bash
streamlit run app.py
How It Works
Ingestion (ingest.py)
PDF
 ├── PyMuPDF extracts text per page → chunked → Documents
 └── PyMuPDF extracts images per page
       └── Gemini Flash describes each image → Documents
              ↓
       Both stored in Chroma (embeddings) + LocalFileStore (raw)
              ↓
       MD5 hash cached → skip re-ingestion on reload
Retrieval + Generation (app.py)
User Question
      ↓
MultiVectorRetriever → top-k text chunks + image descriptions
      ↓
Gemini 1.5 Flash ← text context + raw images (PIL) + question
      ↓
Answer + source images shown in UI
Key Design Decisions
Decision	Reason
PyMuPDF over Unstructured	10x faster, no heavy ML models needed
Gemini Flash over GPT-4o	100% free tier, still multimodal
MD5 cache in JSON	Skip re-ingestion on app reload
LocalFileStore	Persistent docstore across sessions
Max 3 images per query	Stay within free tier rate limits
Skip images < 100×100px	Avoid icons/bullets wasting API calls
Free Tier Limits (Gemini)
Model	Free RPM	Free TPM
Gemini 1.5 Flash	15 req/min	1M tokens/min
embedding-001	1500 req/min	—
✅ More than enough for personal PDF RAG use.

Common Tasks & Fixes
PDF not loading / slow
Use strategy="fast" if switching to Unstructured
PyMuPDF is already the fastest option
Check if PDF is scanned (no text layer) → OCR needed
Images not showing
Check extracted_images/ folder exists
Images < 100×100px are skipped (intentional)
Verify image_path is in Document metadata
Rate limit errors (429)
Gemini Flash: max 15 req/min on free tier
Add time.sleep(4) between image description calls if hitting limits
Re-ingesting same PDF
Delete the entry from ingested_files.json
Or delete chroma_db/ and docstore/ folders to reset everything
Adding multiple PDFs
Call ingest_pdf() for each file — they all share the same Chroma collection
The cache prevents duplicate processing
Improving the System
Better retrieval accuracy
python
# Use MMR (Maximal Marginal Relevance) instead of similarity
retriever.search_type = "mmr"
retriever.search_kwargs = {"k": 6, "fetch_k": 20}
Richer image descriptions
Edit the prompt in utils.py → describe_image_with_gemini():

python
prompt = """Describe this image in extreme detail.
Focus on: exact numbers, axis labels, legend entries,
trend direction, anomalies, and key takeaways."""
Add re-ranking
python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
Environment Variables
Variable	Required	Description
GOOGLE_API_KEY	✅ Yes	From aistudio.google.com
Files Reference
File	Purpose
app.py	Streamlit UI — upload, chat, show images
ingest.py	Parse PDF, describe images, build retriever
utils.py	Gemini image description, base64, resize
requirements.txt	All pip dependencies
.env	API key (never commit to git)
ingested_files.json	MD5 cache of processed PDFs
