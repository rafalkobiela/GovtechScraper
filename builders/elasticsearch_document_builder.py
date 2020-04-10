from typing import Dict


def create_document(text: str, path: str, filename: str) -> Dict[str, str]:
    doc = {
        "text": text,
        "path": path,
        "filename": filename
    }
    return doc
