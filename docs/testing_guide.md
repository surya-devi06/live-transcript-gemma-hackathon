# Testing Guide & Verification Checklist

## 1. Test Architecture

The test suite is structured to separate offline unit/integration tests from external live API calls:

| Test File | Target Module | Requires API Key? | Purpose |
|---|---|---|---|
| `tests/test_transcription.py` | `src/transcriber.py` | No (Offline) | Audio validation, format checks, local Whisper transcription on real speech sample. |
| `tests/test_notes_and_qa.py` | `src/qa_engine.py`, `src/export_utils.py` | No (Mocked) | Verifies lexical retrieval, grounded answering, rejection of unanswerable queries, and multi-format export. |
| `tests/test_app_integration.py` | End-to-end pipeline | No (Mocked LLM) | Validates full pipeline from audio file input to transcript, notes, QA, and export. |
| `tests/test_gemma_connectivity.py` | `src/gemma_client.py` | Yes (Online) | Probes Google Gen AI API, discovers available Gemma models, and runs a live 1-sentence ping. |

---

## 2. Running Automated Tests

Run the full offline test suite:
```powershell
.\.venv\Scripts\python.exe tests\test_transcription.py
.\.venv\Scripts\python.exe tests\test_notes_and_qa.py
.\.venv\Scripts\python.exe tests\test_app_integration.py
```

To run live Gemma connectivity test (requires `GEMINI_API_KEY` set in `.env`):
```powershell
.\.venv\Scripts\python.exe tests\test_gemma_connectivity.py
```

---

## 3. Verification Matrix

- [x] **Application Startup**: Streamlit UI initializes cleanly without syntax or import errors.
- [x] **File Validation**: Non-audio files, empty files, and oversized files (>100MB) are rejected with clear user messages.
- [x] **Local Transcription**: Real speech audio (`samples/sample_speech.wav`) is transcribed locally via Faster-Whisper on CPU with timestamps.
- [x] **Export Formats**: TXT, Markdown, and JSON files are properly generated with correct schemas.
- [x] **Grounded Answering**: Questions directly covered in the transcript receive factual answers with citations.
- [x] **Anti-Hallucination**: Queries on topics absent from the transcript (e.g., "What is the capital of France?") are explicitly rejected as having insufficient evidence.
- [x] **Credential Safety**: No API keys are committed or exposed in UI logs; `.gitignore` guards all private state.
