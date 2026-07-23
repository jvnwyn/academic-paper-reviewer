from collections import Counter
from pathlib import Path
from typing import Any
import re

import fitz  # PyMuPDF


def normalize_line(line: str) -> str:
    """Normalize a line so changing page numbers still count as repeated."""
    line = re.sub(r"\s+", " ", line).strip().lower()
    return re.sub(r"\d+", "#", line)


def get_edge_lines(text: str) -> set[str]:
    """Return likely header/footer lines from the top and bottom of a page."""
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    edge_lines = lines[:3] + lines[-3:]

    return {
        normalize_line(line)
        for line in edge_lines
        if len(line) >= 10
    }


def find_repeated_edge_lines(raw_pages: list[tuple[int, str]]) -> set[str]:
    """
    Find lines occurring on several page edges.

    These are likely running headers/footers rather than paper content.
    """
    if len(raw_pages) < 3:
        return set()

    counts: Counter[str] = Counter()

    for _, text in raw_pages:
        counts.update(get_edge_lines(text))

    # A line must appear on at least 40% of pages, with a minimum of 2 pages.
    minimum_occurrences = max(2, int(len(raw_pages) * 0.4))

    return {
        line
        for line, count in counts.items()
        if count >= minimum_occurrences
    }


def clean_page_text(text: str, repeated_lines: set[str]) -> str:
    """Remove detected headers/footers and normalize PDF text."""
    clean_lines: list[str] = []

    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()

        if not line:
            continue

        if normalize_line(line) in repeated_lines:
            continue

        # Ignore standalone page numbers.
        if line.isdigit():
            continue

        clean_lines.append(line)

    cleaned = " ".join(clean_lines)

    # Join words split at line endings, then normalize spacing.
    cleaned = re.sub(r"(\w)-\s+(\w)", r"\1\2", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)

    return cleaned.strip()


def has_references_heading(text: str) -> bool:
    """Identify the start of a paper's references section."""
    return any(
        normalize_line(line) == "references"
        for line in text.splitlines()
    )

def extract_body_text(page: Any) -> str:
    """
    Extract only the central page area.

    This removes typical running headers and footers by position rather
    than by a paper-specific author or journal name.
    """
    top_bottom_margin = 54  # 0.75 inch in PDF points
    page_height = page.rect.height

    raw_blocks: Any = page.get_text("blocks")
    text_parts: list[str] = []

    for block in raw_blocks:
        _, y0, _, y1, block_text, *_ = block

        if not isinstance(block_text, str):
            continue

        # Ignore blocks in the top or bottom margin.
        if y0 < top_bottom_margin or y1 > page_height - top_bottom_margin:
            continue

        text_parts.append(block_text)

    return "\n".join(text_parts)

def extract_text_from_pdf(pdf_path: Path) -> list[dict[str, object]]:
    """
    Extract cleaned non-empty text from each page of a PDF.

    Returns:
        [
            {"page": 1, "text": "..."},
            {"page": 2, "text": "..."},
        ]
    """
    raw_pages: list[tuple[int, str]] = []

    try:
        with fitz.open(pdf_path) as document:
            for page_index in range(document.page_count):
                page = document.load_page(page_index)
                raw_text = extract_body_text(page)

                if isinstance(raw_text, str) and raw_text.strip():
                    raw_pages.append((page_index + 1, raw_text))

    except fitz.FileDataError as error:
        raise ValueError("The uploaded file could not be read as a PDF.") from error

    repeated_lines = find_repeated_edge_lines(raw_pages)
    pages: list[dict[str, object]] = []
    in_references = False

    for page_number, raw_text in raw_pages:
        # Ignore an INFORMS publisher cover page, not the article itself.
        if "please scroll down for article" in raw_text.lower():
            continue

        if has_references_heading(raw_text):
            in_references = True

        # Exclude bibliography pages from semantic retrieval.
        if in_references:
            continue

        text = clean_page_text(raw_text, repeated_lines)

        if text:
            pages.append({
                "page": page_number,
                "text": text,
            })

    return pages