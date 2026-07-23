import re

from typing import Any, TypedDict

from services.embedding_service import embed_text
from services.vector_service import get_collection

class RetrievedChunk(TypedDict):
    text: str
    page: int
    chunk_id: str
    file_name: str
    distance: float

def is_front_matter_question(question: str) -> bool:
    return bool(re.search(
        r"\b(author|authored|wrote|writer|title|abstract|doi|published|publication year|objective|purpose|goal|aim|main idea|main point|main contribution)\b",
        question,
        flags=re.IGNORECASE,
    ))

def retrieve_relevant_chunks(
    question: str,
    file_name: str,
    limit: int = 5,
) -> list[RetrievedChunk]:
    """Return relevant chunks, prioritizing document metadata when needed."""
    query_embedding = embed_text(question)
    collection = get_collection()

    results: list[RetrievedChunk] = []
    seen_chunk_ids: set[str] = set()

    # For direct questions about paper metadata, place the first-page
    # title/author/abstract chunk before ordinary semantic matches.
    if is_front_matter_question(question):
        front_matter_response: Any = collection.query(
            query_embeddings=[query_embedding],
            n_results=1,
            where={
                "$and": [
                    {"file_name": file_name},
                    {"section": "front_matter"},
                ]
            },
            include=["documents", "metadatas", "distances"],
        )

        for document, metadata, distance in zip(
            front_matter_response["documents"][0],
            front_matter_response["metadatas"][0],
            front_matter_response["distances"][0],
        ):
            if not isinstance(document, str) or not isinstance(metadata, dict):
                continue

            chunk_id = str(metadata["chunk_id"])

            results.append({
                "text": document,
                "page": int(metadata["page"]),
                "chunk_id": chunk_id,
                "file_name": str(metadata["file_name"]),
                "distance": float(distance),
            })
            seen_chunk_ids.add(chunk_id)

    # Retain regular semantic search for the remaining results.
    response: Any = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit,
        where={"file_name": file_name},
        include=["documents", "metadatas", "distances"],
    )

    documents = response["documents"][0]
    metadatas = response["metadatas"][0]
    distances = response["distances"][0]

    for document, metadata, distance in zip(documents, metadatas, distances):
        if not isinstance(document, str) or not isinstance(metadata, dict):
            continue

        chunk_id = str(metadata["chunk_id"])

        if chunk_id in seen_chunk_ids:
            continue

        results.append({
            "text": document,
            "page": int(metadata["page"]),
            "chunk_id": chunk_id,
            "file_name": str(metadata["file_name"]),
            "distance": float(distance),
        })
        seen_chunk_ids.add(chunk_id)

        if len(results) >= limit:
            break

    return results