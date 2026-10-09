
from pathlib import Path

import pytest
from docx import Document

from fs_tools import (
    read_file,
    list_files,
    write_file,
    search_in_file,
)


def test_read_txt(tmp_path):
    file = tmp_path / "resume.txt"
    file.write_text(
        "Python developer with Django experience.",
        encoding="utf-8",
    )

    result = read_file(str(file))

    assert result["success"] is True
    assert "Python" in result["content"]
    assert result["metadata"]["extension"] == ".txt"


def test_read_docx(tmp_path):
    file = tmp_path / "resume.docx"
    document = Document()
    document.add_paragraph("Java developer")
    document.save(file)

    result = read_file(str(file))

    assert result["success"] is True
    assert "Java developer" in result["content"]


def test_read_pdf(tmp_path):
    from pypdf import PdfWriter

    file = tmp_path / "empty.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)

    with file.open("wb") as stream:
        writer.write(stream)

    result = read_file(str(file))

    assert result["success"] is True
    assert result["content"] == ""


def test_read_missing_file(tmp_path):
    result = read_file(str(tmp_path / "missing.txt"))

    assert result["success"] is False
    assert result["error"] is not None


def test_read_unsupported_extension(tmp_path):
    file = tmp_path / "resume.csv"
    file.write_text("name,skills", encoding="utf-8")

    result = read_file(str(file))

    assert result["success"] is False


def test_list_files_and_extension_filter(tmp_path):
    (tmp_path / "a.txt").write_text("A", encoding="utf-8")
    (tmp_path / "b.pdf").write_text("B", encoding="utf-8")
    (tmp_path / "c.TXT").write_text("C", encoding="utf-8")

    all_files = list_files(str(tmp_path))
    txt_files = list_files(str(tmp_path), ".txt")

    assert len(all_files) == 3
    assert len(txt_files) == 2


def test_list_missing_directory(tmp_path):
    assert list_files(str(tmp_path / "missing")) == []


def test_write_creates_directories(tmp_path):
    target = tmp_path / "nested" / "summary.txt"

    result = write_file(str(target), "Resume summary")

    assert result["success"] is True
    assert target.read_text(encoding="utf-8") == "Resume summary"


def test_search_case_insensitive(tmp_path):
    file = tmp_path / "resume.txt"
    file.write_text(
        "Python developer. I also use PYTHON for automation.",
        encoding="utf-8",
    )

    result = search_in_file(str(file), "python")

    assert result["success"] is True
    assert result["match_count"] == 2
    assert len(result["matches"]) == 2


def test_search_no_match(tmp_path):
    file = tmp_path / "resume.txt"
    file.write_text("Java developer", encoding="utf-8")

    result = search_in_file(str(file), "Python")

    assert result["success"] is True
    assert result["match_count"] == 0


def test_search_empty_keyword(tmp_path):
    file = tmp_path / "resume.txt"
    file.write_text("Some text", encoding="utf-8")

    result = search_in_file(str(file), "  ")

    assert result["success"] is False
