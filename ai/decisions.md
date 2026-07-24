# Architectural & Design Decisions

## 1. Local Vector Embeddings
- **Decision:** Use `BAAI/bge-small-en-v1.5` via `sentence-transformers` locally.
- **Reason:** Eliminates API costs, avoids rate limits for document processing, and provides high-quality 384-dimensional retrieval for academic texts.

## 2. Strict Plain Text Gemini Responses
- **Decision:** Instruct Gemini via prompt engineering to write responses in plain text without Markdown formatting (headings, bullet points, asterisks).
- **Reason:** Ensures consistent, clean, unformatted narrative answers in the UI and simplifies citation parsing (`[Page N]`).

## 3. Strict Context Grounding
- **Decision:** Gemini must answer ONLY using provided retrieved excerpts. If missing, Gemini must explicitly report insufficient information.
- **Reason:** Minimizes hallucinations and keeps answers strictly verifiable against the uploaded paper.

## 4. Chunking Parameters
- **Decision:** 700 character chunks with 100 character overlap.
- **Reason:** Optimal context window size for short academic paragraphs while maintaining semantic continuity between chunks.

## 5. Storage & File Naming
- **Decision:** Uploaded files stored in `uploads/` prefixed with `uuid4().hex`. Active document stored in Flask `session['current_file']`.
- **Reason:** Prevents file collision when different users upload files with identical names.
