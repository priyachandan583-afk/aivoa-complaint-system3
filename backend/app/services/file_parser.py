"""
Extracts raw text from uploaded complaint documents.
Production-grade OCR is explicitly NOT required per the assignment brief —
this handles the common text-based formats only.
"""
import email
from email import policy
from io import BytesIO

from docx import Document
from pypdf import PdfReader


def parse_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def parse_docx(file_bytes: bytes) -> str:
    doc = Document(BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs)


def parse_eml(file_bytes: bytes) -> str:
    msg = email.message_from_bytes(file_bytes, policy=policy.default)
    parts = [f"Subject: {msg.get('subject', '')}", f"From: {msg.get('from', '')}"]
    body = msg.get_body(preferencelist=("plain", "html"))
    if body:
        parts.append(body.get_content())
    return "\n".join(parts)


def parse_txt(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")


PARSERS = {
    "pdf": parse_pdf,
    "docx": parse_docx,
    "eml": parse_eml,
    "txt": parse_txt,
}


def extract_text(filename: str, file_bytes: bytes) -> str:
    ext = filename.lower().rsplit(".", 1)[-1]
    parser = PARSERS.get(ext)
    if not parser:
        raise ValueError(f"Unsupported file type: {ext}")
    return parser(file_bytes)
