# Academic Paper Reviewer using Retrieval-Augmented Generation (RAG)

A lightweight Flask web application that uses **Retrieval-Augmented Generation (RAG)** to answer questions about uploaded academic papers. The application retrieves relevant passages from a PDF before generating responses with **Google Gemini**, ensuring answers are grounded in the document rather than relying solely on the language model.

> **Current Status:** In Development (Phase 1 – Core RAG Pipeline)

---

## Features

### Current (MVP)

- Upload academic papers in PDF format
- Extract text using PyMuPDF
- Split documents into semantic chunks
- Generate embeddings using BAAI/bge-small-en-v1.5
- tore embeddings in ChromaDB
- Retrieve relevant document sections using semantic search
- Answer questions using Google Gemini
- Ground responses using retrieved context

---

## Planned Features

- Structured academic paper reviews
- Research paper evaluation
- Methodology analysis
- Novelty assessment
- Strengths and weaknesses analysis
- Multi-document comparison
- Conversational interface
- Export review to PDF or DOCX
- Source page citations
- User authentication

---

# Tech Stack

| Category | Technology |
|----------|------------|
| Backend | Flask |
| Language | Python 3.14+ |
| PDF Processing | PyMuPDF |
| Embeddings | sentence-transformers |
| Embedding Model | BAAI/bge-small-en-v1.5 |
| Vector Database | ChromaDB |
| LLM | Google Gemini |
| Environment | python-dotenv |

---

# Project Structure

```text
academic-reviewer/
│
├── app.py
├── config.py
│
├── models/
│   └── document_chunk.py
│
├── services/
│   ├── pdf_service.py
│   ├── embedding_service.py
│   ├── vector_service.py
│   ├── gemini_service.py
│   └── rag_service.py
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

# System Architecture

```text
                +------------------+
                |   Upload PDF     |
                +--------+---------+
                         |
                         ▼
                +------------------+
                |  Text Extraction |
                |    (PyMuPDF)     |
                +--------+---------+
                         |
                         ▼
                +------------------+
                | Text Chunking    |
                +--------+---------+
                         |
                         ▼
                +------------------+
                | Generate         |
                | Embeddings       |
                +--------+---------+
                         |
                         ▼
                +------------------+
                |   ChromaDB       |
                +--------+---------+
                         |
             User Question
                         |
                         ▼
                +------------------+
                | Similarity Search|
                +--------+---------+
                         |
                         ▼
                +------------------+
                | Google Gemini    |
                +--------+---------+
                         |
                         ▼
                +------------------+
                | Final Response   |
                +------------------+
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/yourusername/academic-reviewer.git
cd academic-reviewer
```

## Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure environment variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Run the application

```bash
python app.py
```

The application will be available at:

```
http://127.0.0.1:5000
```

---

# Development Roadmap

## Phase 1 – Core RAG Pipeline

- [ ] Flask project setup
- [ ] PDF upload
- [ ] Text extraction
- [ ] Text chunking
- [ ] Embedding generation
- [ ] ChromaDB integration
- [ ] Semantic retrieval
- [ ] Gemini integration
- [ ] Question answering

---

## Phase 2 – Academic Reviewer

- [ ] Structured paper summary
- [ ] Novelty analysis
- [ ] Methodology review
- [ ] Strengths and weaknesses
- [ ] Recommendations

---

## Phase 3 – Advanced Features

- [ ] Multi-document comparison
- [ ] Chat interface
- [ ] Export functionality
- [ ] Citation highlighting
- [ ] Authentication

---

# Learning Objectives

This project is designed to deepen understanding of:

- Retrieval-Augmented Generation (RAG)
- Semantic search
- Vector databases
- Embedding models
- Prompt engineering
- Google Gemini API
- Flask application development

---

# License

This project is licensed under the MIT License.

---

# Acknowledgements

- Google Gemini
- ChromaDB
- Sentence Transformers
- Hugging Face
- PyMuPDF
- Flask