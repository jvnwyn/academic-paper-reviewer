from pathlib import Path

import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: Path) -> list[dict[str, object]]:
    """
    Extract non-empty text from each PDF page.

    Returns:
        [
            {"page": 1, "text": "..."},
            {"page": 2, "text": "..."},
        ]
    """
    pages: list[dict[str, object]] = []

    try:
        with fitz.open(pdf_path) as document:
            for page_index in range(document.page_count):
                page = document.load_page(page_index)
                page_number = page_index + 1

                raw_text = page.get_text("text")

                if not isinstance(raw_text, str):
                    continue

                text = raw_text.strip()

                if text:
                    pages.append({
                        "page": page_number,
                        "text": text,
                    })

    except fitz.FileDataError as error:
        raise ValueError("The uploaded file could not be read as a PDF.") from error

    return pages