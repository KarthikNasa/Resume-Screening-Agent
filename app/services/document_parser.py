from pathlib import Path

import fitz
from docx import Document


def extract_pdf_text(file_path: str) -> str:
    """Extract text from a PDF resume."""
    text_parts = []

    with fitz.open(file_path) as pdf:
        for page in pdf:
            text_parts.append(page.get_text())

    return "\n".join(text_parts).strip()


def extract_docx_text(file_path: str) -> str:
    """Extract text from a DOCX resume."""
    document = Document(file_path)

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)


def extract_resume_text(file_path: str) -> str:
    """Extract text based on the file extension."""
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    if extension == ".docx":
        return extract_docx_text(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}. "
        "Only PDF and DOCX are supported."
    )

