from pathlib import Path

from pypdf import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def read_txt(file_path: Path) -> str:
    return file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def read_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def read_docx(file_path: Path) -> str:
    document = Document(str(file_path))

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)


def read_document(file_path: str) -> dict:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dosya bulunamadı: {file_path}"
        )

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Desteklenmeyen dosya türü. "
            "Sadece PDF, DOCX ve TXT destekleniyor."
        )

    if extension == ".txt":
        text = read_txt(path)

    elif extension == ".pdf":
        text = read_pdf(path)

    else:
        text = read_docx(path)

    text = text.strip()

    if not text:
        raise ValueError(
            "Belgeden okunabilir metin çıkarılamadı."
        )

    return {
        "file_name": path.name,
        "file_type": extension.replace(".", ""),
        "text": text,
        "character_count": len(text)
    }