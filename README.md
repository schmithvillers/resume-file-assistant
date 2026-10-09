# Resume File Assistant

An LLM-powered resume file assistant built in Python. The application uses file-system tools and OpenRouter-hosted language models to read resumes, search for skills and experience, and generate summary files.

## 1. Project Overview

This project implements a set of reusable file-system tools and integrates them with a Large Language Model (LLM) through function calling.

The assistant can interpret natural-language requests, select the appropriate tool, execute the operation, and provide a response based on the results.

### Objectives

- Read resumes in PDF, TXT, and DOCX formats.
- List files and retrieve file metadata.
- Write text files and create directories when needed.
- Search resume content using case-insensitive keyword matching.
- Use LLM tool calling to execute file operations based on user requests.
- Generate resume summaries using extracted document content.

## 2. Features

### Core File-System Tools

The `fs_tools.py` module provides four functions:

| Function | Description |
|---|---|
| `read_file(filepath)` | Extracts text from PDF, TXT, and DOCX files and returns content, metadata, and status. |
| `list_files(directory, extension=None)` | Lists files and returns metadata, with optional extension filtering. |
| `write_file(filepath, content)` | Writes UTF-8 text to a file and creates missing parent directories. |
| `search_in_file(filepath, keyword)` | Searches extracted content case-insensitively and returns matching text with surrounding context. |

### LLM Integration

The `llm_file_assistant.py` module integrates the file-system tools with an LLM through the OpenRouter API.

The assistant supports:
- Natural-language requests.
- Automatic tool selection by the LLM.
- Tool execution through a Python dispatcher.
- Returning tool results to the LLM for further reasoning.
- Multiple tool calls within a single request.
- Restrictions on reading and writing files outside designated directories.

## 3. Architecture

The application follows this workflow:

1. The user submits a natural-language request.
2. The LLM interprets the request and selects one or more tools.
3. The Python application validates and dispatches tool calls.
4. The selected function executes the file operation.
5. The result is returned to the LLM.
6. The LLM produces a user-facing response.

### Project Components

- **`fs_tools.py`** — file reading, listing, writing, searching, and metadata extraction.
- **`llm_file_assistant.py`** — OpenRouter integration, tool definitions, dispatching, and conversation loop.
- **`tests/`** — automated tests for file operations and filesystem access restrictions.
- **`sample_data/resumes/`** — fictional sample resumes used for testing.
- **`output/`** — destination for generated summary files.

## 4. Prerequisites

- Python 3.11 or later, subject to dependency and SDK compatibility.
- An OpenRouter account and API key.
- Internet connectivity for LLM requests.
- `pip` for installing dependencies.

The project has been tested in a Python 3.14 virtual environment. If a dependency does not support your Python version, use a compatible Python release.

## 5. Installation and Setup

### Step 1: Clone or download the project

Open a terminal in the project directory.

### Step 2: Create a virtual environment

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a local `.env` file in the project root. You can use `.env.example` as a template.

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key
OPENAI_MODEL=openrouter/free
```

Replace the placeholder with your own API key. Ensure the selected model is available to your account and supports tool calling.

**Security:** Never commit `.env` or expose your API key in source code, screenshots, logs, or the demo video.

### Step 5: Generate sample resumes

If the sample resumes are not already present, run:

```bash
python create_sample_data.py
```

This creates eight fictional resumes in PDF, TXT, and DOCX formats.

## 6. Running the Assistant

From the project root, run:

```bash
python llm_file_assistant.py
```

Enter a natural-language request when the assistant displays the input prompt.

Type `exit` or `quit` to close the application.

## 7. Example Usage

### Example 1: Read All Resumes

**Request**

```text
Read all resumes in the resumes folder.
```

**Expected behavior**

- Lists the available resume files.
- Extracts text from supported files.
- Summarizes the candidates' roles, experience, skills, and education.
- Reports any files that could not be processed.

### Example 2: Find Resumes Mentioning Python

**Request**

```text
Find resumes mentioning Python experience.
```

**Expected behavior**

- Searches the resumes for the requested keyword.
- Returns matching filenames and relevant context.
- Distinguishes matching resumes from non-matching resumes.

Searches are case-insensitive.

### Example 3: Generate a Resume Summary

**Request**

```text
Create a summary file for resume_john_doe.pdf.
```

**Expected behavior**

- Reads the specified resume.
- Generates a summary based on the extracted content.
- Writes the summary to the output directory.
- Reports success only when the file-writing operation succeeds.

The generated file is:

```text
output/john_doe_summary.txt
```

To inspect the generated file on macOS/Linux:

```bash
cat output/john_doe_summary.txt
```

On Windows PowerShell:

```powershell
Get-Content output/john_doe_summary.txt
```

## 8. Running Tests

Run the automated test suite from the project root:

```bash
python -m pytest -v
```

The tests cover:

- TXT and DOCX text extraction.
- PDF extraction.
- Missing and unsupported files.
- File listing and extension filtering.
- Writing files and creating parent directories.
- Case-insensitive searching.
- Empty keywords and missing directories.
- Filesystem access restrictions.

The current test suite contains 15 tests. Run the command above to verify the latest results.

The automated tests do not require live LLM requests for the tested file operations and access restrictions.

## 9. Project Structure

```text
resume-file-assistant/
├── fs_tools.py
├── llm_file_assistant.py
├── create_sample_data.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── tests/
│   ├── test_fs_tools.py
│   └── test_llm_security.py
├── sample_data/
│   └── resumes/
│       ├── john_doe.pdf
│       ├── jane_smith.txt
│       ├── alex_kumar.docx
│       ├── emily_wilson.pdf
│       ├── rahul_mehta.txt
│       ├── sarah_lee.docx
│       ├── michael_brown.pdf
│       └── priya_shah.txt
└── output/
```

Generated files and directories may vary depending on the operations performed.

## 10. Security Considerations

- The LLM requests tool operations; Python executes them through an explicit dispatcher.
- Only registered tools should be executable.
- Resume reads are restricted to the designated resume directory.
- Generated file writes are restricted to the output directory.
- Paths should be resolved and validated before performing file operations.
- API keys are loaded from environment variables rather than hardcoded in source files.
- Resume contents are treated as untrusted input, not as instructions to execute.
- Generated summaries should be checked against the original resume for factual accuracy.

The path restrictions reduce accidental access to unrelated files. They do not replace operating-system permissions or a fully isolated execution environment.

## 11. Limitations

- PDF extraction works for text-based PDFs. Scanned image-only PDFs may require OCR.
- The assistant requires network access and a working OpenRouter API key.
- Model availability, tool-calling behavior, latency, and API costs depend on the selected provider and model.
- Very long resumes may require additional context management or text chunking.
- Generated summaries may omit details and should be checked against the source document.
- File-writing behavior and overwrite handling depend on the implementation of `write_file`.

## 12. Assignment Deliverables

This project is intended to provide the following deliverables:

- `fs_tools.py` with the four required file-system tools.
- `llm_file_assistant.py` with LLM tool calling.
- `requirements.txt` with project dependencies.
- Eight fictional sample resume files.
- Automated tests.
- This README with setup and usage instructions.
- A 2–3 minute demonstration video showing tool calling in action.

## 13. License and Usage

This project was created as an educational assignment demonstrating Python file-system operations, document text extraction, automated testing, and LLM tool calling.

All sample resumes are fictional and intended solely for testing.
