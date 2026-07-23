from typing import Any, TypedDict

from services.embedding_service import embed_text
from services.vector_service import get_collection


class RetrievedChunk(TypedDict):
    text: str
    page: int
    chunk_id: str
    file_name: str
    distance: float


def retrieve_relevant_chunks(
    question: str,
    file_name: str,
    limit: int = 5,
) -> list[RetrievedChunk]:
    """Return the most semantically relevant chunks for a question."""
    query_embedding = embed_text(question)
    collection = get_collection()

    response: Any = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit,
        where={"file_name": file_name},
        include=["documents", "metadatas", "distances"],
    )

    documents = response["documents"][0]
    metadatas = response["metadatas"][0]
    distances = response["distances"][0]

    results: list[RetrievedChunk] = []

    for document, metadata, distance in zip(documents, metadatas, distances):
        if not isinstance(document, str) or not isinstance(metadata, dict):
            continue

        results.append({
            "text": document,
            "page": int(metadata["page"]),
            "chunk_id": str(metadata["chunk_id"]),
            "file_name": str(metadata["file_name"]),
            "distance": float(distance),
        })

    return results