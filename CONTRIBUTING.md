# Contributing to Live Transcript AI

Welcome! We are excited to collaborate on **Live Transcript AI — Powered by Gemma** for the hackathon. This guide outlines our workflow, responsibilities, and coding standards.

---

## 1. Team Roles & Responsibilities

### Project Lead (Surya)
- Repository setup, branch policies, and environment setup.
- Audio input pipeline and local Faster-Whisper transcription integration (`src/transcriber.py`).
- Streamlit UI framework and layout (`app.py`).
- Export manager for TXT, Markdown, and JSON (`src/export_utils.py`).
- Release packaging and submission integration.

### AI & Quality Engineer (Teammate)
- Google Gen AI SDK integration and Gemma model client (`src/gemma_client.py`).
- Structured notes prompt engineering and concept extractor (`src/notes_generator.py`).
- Grounded Q&A engine, segment retrieval, and anti-hallucination guard (`src/qa_engine.py`).
- Automated test suites (`tests/`) and documentation review.

---

## 2. Git Workflow & Branching Strategy

To keep our commit history genuine and clean:
1. `main` (or `master`): Always production-ready, passing all tests.
2. Feature branches:
   - `feat/transcription-engine`: Transcription & audio validation
   - `feat/gemma-notes`: Gemma client & note generation
   - `feat/grounded-qa`: QA engine & retrieval
   - `feat/ui-export`: Streamlit interface & multi-format export
   - `test/integration-suite`: End-to-end tests and test fixtures
3. **Pull Requests**:
   - Every feature must be submitted via a Pull Request.
   - Describe what was added and link the corresponding GitHub issue.
   - Include test results before requesting a merge review.

---

## 3. Pull Request Review Checklist

Before approving and merging a PR:
- [ ] Code follows PEP 8 style standards and includes clear docstrings.
- [ ] All tests run and pass locally (`pytest` or test runner scripts).
- [ ] No secrets, API keys, or `.env` files are tracked by Git.
- [ ] Error handling is in place for missing credentials, invalid input, or API outages.
- [ ] UI elements are responsive and intuitive.

---

## 4. Local Development Setup

```bash
# Clone the repository
git clone <repo-url>
cd <repo-folder>

# Set up virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # Windows PowerShell
# source .venv/bin/activate     # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Run automated tests
python tests/test_transcription.py
python tests/test_notes_and_qa.py
python tests/test_app_integration.py

# Launch application
streamlit run app.py
```
