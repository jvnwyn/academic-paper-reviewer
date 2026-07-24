# Project.md

# Academic Paper Reviewer using Retrieval-Augmented Generation (RAG)

## Project Overview

The Academic Paper Reviewer is a lightweight web application that enables users to upload an academic paper in PDF format and ask questions about its contents. The application uses a **Retrieval-Augmented Generation (RAG)** pipeline to retrieve relevant sections from the uploaded paper before generating responses with **Google Gemini**.

The primary goal of the first development phase is to build a reliable and explainable RAG pipeline. Advanced review features such as structured evaluations and multi-document analysis will be added after the core functionality is complete.

---

# Objectives

## Primary Objective

Develop a Flask-based RAG application capable of answering questions about an uploaded academic paper using only information retrieved from the document.

## Secondary Objectives

- Upload academic papers in PDF format.
- Extract and preprocess text from research papers.
- Generate semantic embeddings.
- Store embeddings in a vector database.
- Retrieve relevant document chunks.
- Generate grounded responses using Google Gemini.

---

# Tech Stack

## Backend

- Flask

## Programming Language

- Python 3.14+

## PDF Processing

- PyMuPDF

## Embedding Model

- sentence-transformers
- Model: `BAAI/bge-small-en-v1.5`

## Vector Database

- ChromaDB

## Large Language Model

- Google Gemini

## Environment Variables

- python-dotenv

## Numerical Computing

- NumPy

---

# Project Structure

```text
academic-reviewer/
│
├── app.py                     # Flask application
├── config.py                  # Application configuration
│
├── services/
│   ├── pdf_service.py         # Extract text from PDF
│   ├── embedding_service.py   # Generate embeddings
│   ├── vector_service.py      # ChromaDB operations
│   ├── gemini_service.py      # Gemini API integration
│   └── rag_service.py         # RAG orchestration
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   └── js/
│
├── uploads/
├── chroma_db/
│
├── requirements.txt
├── .env
├── README.md
└── Project.md
```

---

# System Workflow

```text
User Uploads PDF
        │
        ▼
Extract Text (PyMuPDF)
        │
        ▼
Split into Chunks
        │
        ▼
Generate Embeddings
        │
        ▼
Store in ChromaDB
        │
        ▼
User Asks Question
        │
        ▼
Retrieve Relevant Chunks
        │
        ▼
Google Gemini
        │
        ▼
Generate Answer
```

---

# Core Features (MVP)

## 1. PDF Upload

Users can upload a single academic paper in PDF format.

### Input

- PDF file

### Output

- Successfully uploaded document

---

## 2. PDF Text Extraction

Extract readable text from every page of the uploaded PDF.

### Responsibilities

- Read PDF pages
- Preserve page numbers
- Ignore non-text elements when possible

### Output

```python
[
    {
        "page": 1,
        "text": "..."
    },
    {
        "page": 2,
        "text": "..."
    }
]
```

---

## 3. Text Chunking

Split extracted text into overlapping chunks suitable for semantic search.

### Configuration

- Chunk Size: 700 characters
- Chunk Overlap: 100 characters

Each chunk retains metadata such as:

- Page number
- Chunk ID

---

## 4. Embedding Generation

Generate vector embeddings for every chunk using:

```
BAAI/bge-small-en-v1.5
```

Output:

```text
Chunk
↓

Embedding Vector
```

---

## 5. Vector Storage

Store embeddings inside ChromaDB.

Each record contains:

- Chunk text
- Embedding
- Page number
- Chunk ID
- File name

---

## 6. Semantic Retrieval

When a user asks a question:

1. Convert the question into an embedding.
2. Perform similarity search.
3. Retrieve the Top-5 most relevant chunks.

---

## 7. Answer Generation

The retrieved chunks are passed to Google Gemini together with the user's question.

Gemini should answer **only using the retrieved context**.

If the answer cannot be found in the retrieved context, Gemini should clearly state that there is insufficient information.

---

# Prompting Strategy

## System Prompt

```text
You are an academic assistant.

Answer ONLY using the provided context.

Do not make assumptions or fabricate information.

If the answer is not contained in the context, say that the paper does not provide enough information.

Whenever possible, reference the page numbers associated with the retrieved context.
```

---

# Phase 1 Development Plan

## Milestone 1

- Flask project setup
- PDF upload
- Status: Complete

---

## Milestone 2

- PDF text extraction
- Status: Complete

---

## Milestone 3

- Text chunking
- Status: Complete

---

## Milestone 4

- Embedding generation
- Status: Complete

---

## Milestone 5

- ChromaDB integration
- Status: Complete

---

## Milestone 6

- Semantic retrieval
- Status: Complete

---

## Milestone 7

- Gemini integration
- Status: Complete

---

## Milestone 8

- End-to-end question answering
- Status: Complete
- Verified by uploading a PDF, asking a natural-language question, generating a Gemini answer, and displaying relevant source sections with page/chunk references.

---

# Success Criteria

The MVP is complete when the application can:

- Upload an academic paper.
- Extract its text correctly.
- Generate semantic embeddings.
- Store embeddings in ChromaDB.
- Retrieve relevant document chunks.
- Answer user questions using retrieved context.
- Minimize hallucinations by grounding responses in the uploaded paper.

---

# Future Enhancements

These features are intentionally excluded from the MVP and will be implemented in later phases.

- Structured academic paper review
- Research paper scoring
- Methodology evaluation
- Novelty analysis
- Strength and weakness analysis
- Multi-document comparison
- Conversation history
- PDF highlighting
- Export to PDF or DOCX
- User authentication