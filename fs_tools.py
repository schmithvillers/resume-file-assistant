
"""
fs_tools.py

File-system utilities for reading, listing, writing, and searching
resume files in PDF, TXT, and DOCX formats.
"""

from pathlib import Path
from datetime import datetime
import os

from pypdf import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx"}


def _file_metadata(path: Path) -> dict:
    """Return basic metadata for a file."""
    stat = path.stat()
    return {
        "filename": path.name,
        "extension": path.suffix.lower(),
        "size_bytes": stat.st_size,
        "modified_time": datetime.fromtimestamp(
            stat.st_mtime
        ).isoformat(timespec="seconds"),
    }


def _extract_text(path: Path) -> str:
    """Extract text from a supported file."""
    extension = path.suffix.lower()

    if extension == ".txt":
        # utf-8-sig also handles a UTF-8 byte-order mark.
        try:
            return path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            return path.read_text(encoding="latin-1")

    if extension == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    if extension == ".docx":
        document = Document(str(path))
        paragraphs = [p.text for p in document.paragraphs]
        return "\n".join(paragraphs)

    raise ValueError(
        f"Unsupported file extension: {extension or '(none)'}"
    )


def read_file(filepath: str) -> dict:
    """
    Read a PDF, TXT, or DOCX file.

    Returns a dictionary containing extracted content, metadata,
    and a success/error status.
    """
    path = Path(filepath).expanduser()

    try:
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {filepath}")

        content = _extract_text(path)

        return {
            "success": True,
            "filepath": str(path.resolve()),
            "content": content,
            "metadata": {
                **_file_metadata(path),
                "character_count": len(content),
                "page_count": (
                    len(PdfReader(str(path)).pages)
                    if path.suffix.lower() == ".pdf"
                    else None
                ),
            },
            "error": None,
        }

    except Exception as exc:
        return {
            "success": False,
            "filepath": str(path),
            "content": None,
            "metadata": None,
            "error": f"{type(exc).__name__}: {exc}",
        }


def list_files(directory: str, extension: str = None) -> list:
    """
    List files directly inside a directory.

    If extension is provided, filter by it, e.g. '.pdf'.
    Matching is case-insensitive.

    Returns a list of metadata dictionaries. An invalid directory
    produces an empty list.
    """
    path = Path(directory).expanduser()

    if not path.is_dir():
        return []

    normalized_extension = None
    if extension:
        normalized_extension = extension.lower()
        if not normalized_extension.startswith("."):
            normalized_extension = "." + normalized_extension

    results = []

    try:
        for item in sorted(path.iterdir(), key=lambda p: p.name.lower()):
            if not item.is_file():
                continue

            if (
                normalized_extension is not None
                and item.suffix.lower() != normalized_extension
            ):
                continue

            try:
                results.append({
                    **_file_metadata(item),
                    "path": str(item.resolve()),
                })
            except OSError:
                # Skip files whose metadata cannot be accessed.
                continue

    except OSError:
        return []

    return results


def write_file(filepath: str, content: str) -> dict:
    """
    Write UTF-8 text to a file, creating parent directories.

    Existing files are overwritten. Callers should restrict output
    paths and confirm overwrites when appropriate.
    """
    path = Path(filepath).expanduser()

    try:
        if not isinstance(content, str):
            raise TypeError("content must be a string")

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "filepath": str(path.resolve()),
            "bytes_written": path.stat().st_size,
            "error": None,
        }

    except Exception as exc:
        return {
            "success": False,
            "filepath": str(path),
            "bytes_written": 0,
            "error": f"{type(exc).__name__}: {exc}",
        }


def search_in_file(filepath: str, keyword: str) -> dict:
    """
    Search extracted file text for a keyword, ignoring case.

    Each match includes a short context window around the occurrence.
    """
    if not isinstance(keyword, str) or not keyword.strip():
        return {
            "success": False,
            "filepath": str(filepath),
            "keyword": keyword,
            "match_count": 0,
            "matches": [],
            "error": "keyword must be a non-empty string",
        }

    result = read_file(filepath)

    if not result["success"]:
        return {
            "success": False,
            "filepath": str(filepath),
            "keyword": keyword,
            "match_count": 0,
            "matches": [],
            "error": result["error"],
        }

    content = result["content"]
    search_term = keyword.strip()
    lower_content = content.lower()
    lower_term = search_term.lower()

    matches = []
    start = 0
    context_radius = 80

    while True:
        index = lower_content.find(lower_term, start)
        if index == -1:
            break

        context_start = max(0, index - context_radius)
        context_end = min(
            len(content), index + len(search_term) + context_radius
        )

        matches.append({
            "match": content[index:index + len(search_term)],
            "position": index,
            "context": content[context_start:context_end],
        })

        start = index + len(search_term)

    return {
        "success": True,
        "filepath": result["filepath"],
        "keyword": search_term,
        "match_count": len(matches),
        "matches": matches,
        "error": None,
    }
