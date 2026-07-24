# System Architecture

## Overview
Lightweight Flask application hosting a Retrieval-Augmented Generation (RAG) pipeline for PDF academic papers.

## Component Breakdown

```
[Web UI (index.html)] <--> [Flask App (app.py)]
                                  |
                                  v
                       [RAG Service (rag_service.py)]
                               /         \
                              /           \
                             v             v
             [Retrieval Service]        [Gemini Service]
             (retrieval_service.py)     (gemini_service.py)
                    |
                    v
             [ChromaDB Vector Store]
             (vector_service.py)
```

### Services Layer (`services/`)
- `pdf_service.py`: Uses PyMuPDF (`fitz`) to extract page-by-page text. Validates PDF structure and detects unreadable/scanned PDFs.
- `chunking_service.py`: Implements RAG01 (700 char chunk size, 100 char overlap). Maintains page numbers and chunk IDs.
- `embedding_service.py`: Implements EMB01 (`BAAI/bge-small-en-v1.5` model via `sentence-transformers`). Generates 384-dim vector embeddings.
- `vector_service.py`: Implements VEC01 (ChromaDB persistent client). Handles chunk collection `academic_paper_chunks` storage & deletion.
- `retrieval_service.py`: Performs vector similarity search in ChromaDB filtered by active PDF `file_name` to retrieve top-5 chunks.
- `gemini_service.py`: Implements GEM01 (`google-genai` SDK using `gemini-3.6-flash`). Calls Gemini API with strict system prompt.
- `rag_service.py`: High-level orchestrator connecting retrieval and Gemini answer generation.
