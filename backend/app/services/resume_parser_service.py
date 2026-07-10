from backend.app.utils.pdf_parser import extract_text_from_pdf


def normalize_text(text: str) -> str:
    """
    Normalize extracted PDF text.

    Future improvements:
    - Fix ligatures
    - Remove duplicated whitespace
    - Unicode normalization
    """

    return " ".join(text.split())


def parse_resume(file_path: str) -> dict:
    """
    Parse a resume PDF.

    Returns:
        {
            "raw_text": "...",
            "normalized_text": "...",
            "character_count": 1234,
            "word_count": 250,
        }
    """

    raw_text = extract_text_from_pdf(file_path)

    normalized_text = normalize_text(raw_text)

    return {
        "raw_text": raw_text,
        "normalized_text": normalized_text,
        "character_count": len(normalized_text),
        "word_count": len(normalized_text.split()),
    }
