from typing import Any, TypedDict

from sentence_transformers import SentenceTransformer

from config import Config
from services.chunking_service import TextChunk


class EmbeddedChunk(TextChunk):
    embedding: list[float]


_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    """Load the embedding model once, then reuse it."""
    global _model

    if _model is None:
        _model = SentenceTransformer(Config.EMBEDDING_MODEL)

    return _model


def generate_embeddings(chunks: list[TextChunk]) -> list[EmbeddedChunk]:
    """Add a normalized embedding vector to every text chunk."""
    if not chunks:
        return []

    texts = [chunk["text"] for chunk in chunks]
    model = get_embedding_model()

    vectors: Any = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    embedded_chunks: list[EmbeddedChunk] = []

    for chunk, vector in zip(chunks, vectors):
        embedding = [float(value) for value in vector.tolist()]

        embedded_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "page": chunk["page"],
            "text": chunk["text"],
            "embedding": embedding,
        })

    return embedded_chunks