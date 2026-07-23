from typing import TypedDict


class TextChunk(TypedDict):
    chunk_id: str
    page: int
    text: str


def chunk_pages(
    pages: list[dict[str, object]],
    chunk_size: int = 700,
    chunk_overlap: int = 100,
) -> list[TextChunk]:
    """Split extracted PDF pages into overlapping text chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be between 0 and chunk_size - 1.")

    chunks: list[TextChunk] = []
    step_size = chunk_size - chunk_overlap
    chunk_number = 1

    for page_data in pages:
        page_number = page_data.get("page")
        page_text = page_data.get("text")

        # Ensures the values have the correct types.
        if not isinstance(page_number, int) or not isinstance(page_text, str):
            continue

        start = 0

        while start < len(page_text):
            end = start + chunk_size
            chunk_text = page_text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "chunk_id": f"chunk_{chunk_number:04d}",
                    "page": page_number,
                    "text": chunk_text,
                })
                chunk_number += 1

            if end >= len(page_text):
                break

            start += step_size

    return chunks