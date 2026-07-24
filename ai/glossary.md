# Domain Terminology & Stable IDs

## Stable IDs
- **RAG01:** Chunking configuration (700 characters, 100 character overlap, preserving page metadata).
- **EMB01:** `BAAI/bge-small-en-v1.5` sentence-transformer model producing 384-dimensional dense vectors.
- **VEC01:** Persistent ChromaDB instance storing document chunks with similarity query support.
- **GEM01:** `google-genai` SDK integration with `gemini-3.6-flash`, strictly grounded prompt, and `[Page N]` citation requirement.

## Terminology
- **RAG:** Retrieval-Augmented Generation — retrieving relevant context from vector database before passing to LLM.
- **Top-5 Retrieval:** Selecting the 5 highest cosine-similarity chunks matching the user's question embedding.
- **Grounded Answer:** LLM response derived strictly from provided context without introducing external pre-trained knowledge.
