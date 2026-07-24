# PROJECT HANDOFF

## 1. Identity
- **Name:** Academic Paper Reviewer
- **Type:** RAG-based Academic Paper Q&A Web Application
- **Stack:** Python 3.14+, Flask 3.1, PyMuPDF, sentence-transformers (`BAAI/bge-small-en-v1.5`), ChromaDB, Google Gemini (`gemini-3.6-flash`)

## 2. Goal
Enable researchers to upload PDF academic papers and ask questions, receiving answers strictly grounded in paper text with page citations (`[Page N]`) to eliminate LLM hallucinations.

## 3. Architecture
- **Frontend:** Flask Jinja2 templates (`templates/index.html`), HTML, Vanilla CSS/JS.
- **Backend:** Flask web server (`app.py`), modular service layer (`services/`).
- **Data Flow:** `PDF Upload` -> `PyMuPDF Extraction` -> `Chunking` -> `BGE Embeddings` -> `ChromaDB Store` -> `Top-5 Retrieval` -> `Gemini Generation`.
- **Vector DB:** ChromaDB persistent storage (`chroma_db/`, collection `academic_paper_chunks`).
- **LLM:** Google Gemini via `google-genai` SDK with thinking level `low`.

## 4. Current State
### Phase 1 (MVP) - DONE
- ✓ PDF Upload & Validation (`allowed_pdf`)
- ✓ PDF Text Extraction per page (`services/pdf_service.py`)
- ✓ Text Chunking (700 chars / 100 overlap) (`services/chunking_service.py`)
- ✓ Local Vector Embeddings (`services/embedding_service.py`)
- ✓ ChromaDB Storage & Querying (`services/vector_service.py`, `retrieval_service.py`)
- ✓ Document-Grounded Answer Generation (`services/gemini_service.py`, `rag_service.py`)
- ✓ Web UI for PDF Upload & Question Answering (`templates/index.html`)

### Phase 2 - NEXT
- △ Multi-document paper comparison
- ✗ Structured paper review & scoring (novelty, methodology, strengths/weaknesses)
- ✗ PDF text highlighting & line reference
- ✗ Conversation history & export to PDF/DOCX
- ✗ User authentication

## 5. Decisions
- **Local Embedding Model:** Use `BAAI/bge-small-en-v1.5` locally via `sentence-transformers` to avoid embedding API costs and network latency.
- **RAG Grounding Strategy (GEM01):** Gemini prompt strictly forbids outside knowledge; requires direct answer in plain text (no markdown headings/bullets) and mandatory page citations (`[Page N]`).
- **Chunking Parameters (RAG01):** 700-character chunks with 100-character overlap preserving page number metadata.
- **ChromaDB Metadata:** Store `file_name`, `page`, `chunk_id`, and `text` with each vector for precise single-paper filtering.
- **Session Tracking:** Current active uploaded file stored in Flask `session['current_file']`.

## 6. Rules
- Ground answers strictly in retrieved context; state "insufficient information" if context is missing.
- Gemini responses must be plain text without Markdown formatting (bullets, bold, headings).
- Maintain service encapsulation (one responsibility per file in `services/`).
- Always validate uploaded files for MIME header (`%PDF-`) and size limit (25 MB).

## 7. Known Issues
- Scanned PDFs without embedded text layers fail text extraction (returns warning).
- Initial load of `BAAI/bge-small-en-v1.5` embedding model has cold-start delay.

## 8. Stable IDs
- **RAG01:** Chunking 700 chars / 100 overlap + page metadata.
- **EMB01:** `BAAI/bge-small-en-v1.5` 384-dim embeddings.
- **VEC01:** ChromaDB persistent storage & Top-5 similarity search filtered by `file_name`.
- **GEM01:** `google-genai` client, model `gemini-3.6-flash`, strict grounding system prompt.

## 9. Key Files
- `app.py`: Flask entry point & HTTP routes (`/`, `/upload`, `/ask`)
- `config.py`: App configuration & environment settings
- `services/pdf_service.py`: PyMuPDF text extraction
- `services/chunking_service.py`: Text chunking implementation
- `services/embedding_service.py`: SentenceTransformer model management
- `services/vector_service.py`: ChromaDB initialization & CRUD
- `services/retrieval_service.py`: Semantic top-k search
- `services/gemini_service.py`: Gemini client & prompt generation
- `services/rag_service.py`: RAG orchestration
- `templates/index.html`: Web interface

## 10. AI Instructions
1. Respect modular service boundaries in `services/`.
2. Do not introduce unnecessary dependencies outside `requirements.txt`.
3. Preserve plain text output constraint for Gemini generation.
4. Always pass page metadata along with chunk vectors.
5. Ask before modifying core RAG parameters (chunk size, embedding model, LLM system prompt).
