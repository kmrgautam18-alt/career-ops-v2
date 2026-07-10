import fitz


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract plain text from a PDF.

    Args:
        file_path: Absolute path of the PDF.

    Returns:
        Extracted text.
    """

    document = fitz.open(file_path)

    text = []

    try:
        for page in document:
            text.append(page.get_text())
    finally:
        document.close()

    return "\n".join(text).strip()
