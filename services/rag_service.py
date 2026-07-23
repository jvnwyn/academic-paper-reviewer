from typing import TypedDict

from services.gemini_service import generate_answer
from services.retrieval_service import RetrievedChunk, retrieve_relevant_chunks


class RAGResponse(TypedDict):
    answer: str
    sources: list[RetrievedChunk]


def answer_question(question: str, file_name: str) -> RAGResponse:
    """Retrieve paper excerpts, then use them as Gemini's answer context."""
    sources = retrieve_relevant_chunks(question, file_name)

    if not sources:
        return {
            "answer": "I could not find relevant sections in the uploaded paper.",
            "sources": [],
        }

    context_parts: list[str] = []

    for source in sources:
        context_parts.append(
            f"[Page {source['page']} · {source['chunk_id']}]\n"
            f"{source['text']}"
        )

    context = "\n\n---\n\n".join(context_parts)
    answer = generate_answer(question, context)

    return {
        "answer": answer,
        "sources": sources,
    }