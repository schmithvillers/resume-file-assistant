
"""Automated tests for filesystem access restrictions."""

import os

# Allow importing the assistant during tests without a real API key.
os.environ.setdefault("OPENROUTER_API_KEY", "test-key-for-local-tests")

from pathlib import Path

from llm_file_assistant import safe_read_file, safe_write_file


def test_read_outside_resume_directory_is_rejected():
    result = safe_read_file("../../.env")

    assert result["success"] is False
    assert "not allowed" in result["error"].lower()


def test_write_outside_output_directory_is_rejected(
    tmp_path, monkeypatch
):
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    monkeypatch.setattr(
        "llm_file_assistant.OUTPUT_DIR", output_dir
    )

    result = safe_write_file("../outside.txt", "test")

    assert result["success"] is False
    assert not (tmp_path / "outside.txt").exists()


def test_write_inside_output_directory_is_allowed(
    tmp_path, monkeypatch
):
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    monkeypatch.setattr(
        "llm_file_assistant.OUTPUT_DIR", output_dir
    )

    result = safe_write_file("summary.txt", "Test summary")

    assert result["success"] is True
    assert (output_dir / "summary.txt").read_text(
        encoding="utf-8"
    ) == "Test summary"


def test_read_outside_resume_directory_is_rejected_with_absolute_path(
    tmp_path, monkeypatch
):
    resume_dir = tmp_path / "resumes"
    resume_dir.mkdir()

    secret_file = tmp_path / "secret.txt"
    secret_file.write_text("private content", encoding="utf-8")

    monkeypatch.setattr(
        "llm_file_assistant.RESUME_DIR", resume_dir
    )

    result = safe_read_file(str(secret_file))

    assert result["success"] is False
    assert "not allowed" in result["error"].lower()
