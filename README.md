# Academic Paper Reviewer using Retrieval-Augmented Generation (RAG)

A lightweight Flask web application that uses **Retrieval-Augmented Generation (RAG)** to answer questions about uploaded academic papers. The application retrieves relevant passages from a PDF before generating responses with **Google Gemini**, ensuring answers are grounded in the uploaded document.

> **Current Status:** Phase 1 Complete - Core RAG Pipeline with End-to-End Question Answering

---

## Features

### Current MVP

- Upload academic papers in PDF format
- Validate uploaded PDF files
- Extract text using PyMuPDF
- Split documents into semantic chunks
- Generate embeddings using `BAAI/bge-small-en-v1.5`
- Store embeddings in ChromaDB
- Retrieve relevant document sections using semantic search
- Generate grounded answers using Google Gemini
- Display relevant source sections with page and chunk references

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
- PDF highlighting
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
| Environment Variables | python-dotenv |

---

# Project Structure

```text
academic-paper-reviewer/
|
|-- app.py
|-- config.py
|
|-- services/
|   |-- pdf_service.py
|   |-- chunking_service.py
|   |-- embedding_service.py
|   |-- vector_service.py
|   |-- retrieval_service.py
|   |-- gemini_service.py
|   |-- rag_service.py
|
|-- templates/
|   |-- index.html
|
|-- static/
|   |-- css/
|   |-- js/
|
|-- uploads/
|-- chroma_db/
|
|-- requirements.txt
|-- .env
|-- README.md
|-- Project.md
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

Create a `.env` file in the project root:

```text
academic-paper-reviewer/.env
```

Use this template:

```env
SECRET_KEY=replace-this-with-a-long-random-secret
GEMINI_API_KEY=your_google_ai_studio_api_key
HF_TOKEN=your_huggingface_token_here
```

---

## Generate a Flask secret key

`SECRET_KEY` is used by Flask to protect sessions and flash messages.

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated value into `SECRET_KEY`.

---

## Get a Gemini API key

`GEMINI_API_KEY` is used to call Google Gemini for answer generation.

Create a key from Google AI Studio:

```text
https://aistudio.google.com/app/apikey
```

Copy the key into `GEMINI_API_KEY`.

---

## Get a Hugging Face token

`HF_TOKEN` is used to authenticate Hugging Face model downloads and enable higher rate limits.

Create a read-only token from Hugging Face:

```text
https://huggingface.co/settings/tokens
```

Copy the token into `HF_TOKEN`.

Example `.env`:

```env
SECRET_KEY=your_generated_flask_secret_key
GEMINI_API_KEY=your_google_ai_studio_api_key
HF_TOKEN=hf_your_huggingface_token
```

Do not commit `.env` to Git.

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

- [x] Flask project setup
- [x] PDF upload
- [x] Text extraction
- [x] Text chunking
- [x] Embedding generation
- [x] ChromaDB integration
- [x] Semantic retrieval
- [x] Gemini integration
- [x] Question answering

---

## Phase 2 – Academic Reviewer

- [-] Structured paper summary
- [-] Novelty analysis
- [-] Methodology review
- [-] Strengths and weaknesses
- [-] Recommendations

---

## Phase 3 – Advanced Features

- [-] Multi-document comparison
- [-] Chat interface
- [-] Export functionality
- [-] Citation highlighting
- [-] Authentication

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
