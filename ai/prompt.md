# AI Operating Instructions

## Rules for AI Assistant
1. **Respect Architecture:** Keep services strictly inside `services/` and maintain single-responsibility modules (`pdf_service`, `chunking_service`, `embedding_service`, `vector_service`, `retrieval_service`, `gemini_service`, `rag_service`).
2. **Preserve Coding Style:** Follow standard Python practices (type hinting, PEP 8 formatting, exception handling).
3. **No Unrequested Dependencies:** Do not add external packages without explicit approval.
4. **Preserve Output Rules:** Gemini prompt must enforce strict context grounding and plain-text output with page citations (`[Page N]`).
5. **Ask Before Major Refactoring:** Always ask before changing chunking parameters, embedding models, vector store setup, or LLM providers.
