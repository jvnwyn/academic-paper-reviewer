from hashlib import sha256
from typing import Any

import chromadb

from config import Config
from services.embedding_service import EmbeddedChunk


def get_collection() -> Any:
    """Return the persistent collection used for paper chunks."""
    client = chromadb.PersistentClient(
        path=str(Config.CHROMA_DB_PATH),
    )

    return client.get_or_create_collection(
        name=Config.CHROMA_COLLECTION_NAME,
    )


def store_document_chunks(
    embedded_chunks: list[EmbeddedChunk],
    file_name: str,
) -> int:
    """
    Store a paper's chunks and embeddings in ChromaDB.

    Existing chunks belonging to this filename are replaced.
    """
    if not embedded_chunks:
        return 0

    collection = get_collection()

    # Re-uploading the same paper replaces its old stored chunks.
    collection.delete(where={"file_name": file_name})

    file_hash = sha256(file_name.encode("utf-8")).hexdigest()[:16]

    ids: list[str] = []
    documents: list[str] = []
    embeddings: list[list[float]] = []
    metadatas: list[dict[str, str | int]] = []

    for chunk in embedded_chunks:
        ids.append(f"{file_hash}_{chunk['chunk_id']}")
        documents.append(chunk["text"])
        embeddings.append(chunk["embedding"])
        metadatas.append({
            "file_name": file_name,
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(ids)