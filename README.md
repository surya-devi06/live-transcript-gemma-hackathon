# Live Transcript AI — Powered by Google Gemma

> Transform spoken content into searchable transcripts, intelligent notes, and interactive learning.

Live Transcript AI is an open-source tool built for **Otaku.dev '26 — Hacktoberfest Hack Day, Chennai**. It transforms spoken audio and educational video recordings into searchable transcripts and structured, AI-synthesized learning materials powered by **Google Gemma 4**.

---

## 🎯 Key Features

1. **Audio & Video Ingestion**: Supports `.mp3`, `.wav`, `.m4a`, `.mp4`, `.webm`, and `.ogg` uploads with strict size and format validation (up to 100MB).
2. **Local, Privacy-First Speech Recognition**: Powered by Faster-Whisper running on-device with int8 CPU quantization—delivering fast timestamps and full privacy with zero audio transmission.
3. **Structured Notes via Google Gemma 4**: Leverages `gemma-4-26b-a4b-it` (via the official Google Gen AI SDK) to generate hierarchical study notes, executive summaries, key terms, takeaways, and real-world applications.
4. **Grounded Q&A (Anti-Hallucination)**: Interactive question-answering strictly anchored in transcript evidence; declines out-of-context queries with clear "insufficient evidence" notices.
5. **Multi-Format Export**: One-click download of verbatim transcripts (`.txt`), formatted study guides (`.md`), and comprehensive structured payloads (`.json`).
6. **Demo-Ready Sample**: Includes a pre-bundled audio fixture (`samples/sample_speech.wav`) for instant testing without manual file uploads.

---

## 🏗️ Architecture & Technology Stack

```
+-------------------------------------------------------------+
|                     User Browser (UI)                       |
|               Streamlit Responsive Interface                |
+------------------------------+------------------------------+
                               |
            (Audio Upload / Sample Selection)
                               v
+-------------------------------------------------------------+
|              Validation & Audio Transcriber                 |
|             (Faster-Whisper on CPU / int8)                  |
+------------------------------+------------------------------+
                               |
               (Clean Timestamped Transcript)
                               v
               +---------------+---------------+
               |                               |
               v                               v
+------------------------------+ +----------------------------+
|        NotesGenerator        | |          QAEngine          |
|      (Google Gemma 4)        | |      (Google Gemma 4)      |
|  - Executive Summary         | |  - Lexical Keyword Index   |
|  - Key Concepts              | |  - Grounded Evidence RAG   |
|  - Study Notes               | |  - Anti-Hallucination Guard|
+--------------+---------------+ +--------------+-------------+
               |                               |
               +---------------+---------------+
                               |
                               v
+-------------------------------------------------------------+
|                        ExportManager                        |
|             Export TXT / Markdown (.md) / JSON              |
+-------------------------------------------------------------+
```

* **Frontend**: Streamlit
* **Speech-to-Text**: Faster-Whisper (CTranslate2 backend)
* **LLM Engine**: Google Gemma 4 (`gemma-4-26b-a4b-it`) via Google Gen AI SDK (`google-genai`)
* **Fallbacks**: `gemma-3-27b-it`, `gemma-3-12b-it`, `gemma-2-27b-it`
* **Configuration**: python-dotenv
* **Testing**: Pytest & Python standard unittest

---

## 🚀 Setup & Installation

### 1. Prerequisites
* Python 3.10+ (64-bit)
* Git
* Free Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/surya-devi06/Live-Transcript-AI-Gemma-4-Hackathon-Project.git
cd Live-Transcript-AI-Gemma-4-Hackathon-Project

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate    # Linux / macOS

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Create local .env from example template
cp .env.example .env
```

Edit `.env` to include your API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
GEMMA_MODEL_ID=gemma-4-26b-a4b-it
```
*(Alternatively, enter your API key directly in the Streamlit UI sidebar.)*

### 4. Running the Application

```bash
streamlit run app.py
```

---

## 🧪 Testing & Verification

Run the automated offline test suite:
```bash
python tests/test_transcription.py
python tests/test_notes_and_qa.py
python tests/test_app_integration.py
```

To test live Gemma API connectivity (requires `GEMINI_API_KEY` set in `.env`):
```bash
python tests/test_gemma_connectivity.py
```

---

## 👥 Team & Contributions

| Member | Role | Key Contributions |
|---|---|---|
| **Surya (Lead)** | Project Lead & Fullstack Engineer | Repository architecture, Faster-Whisper local pipeline, Streamlit UI, Export manager, end-to-end integration |
| **Teammate** | AI & Quality Engineer | Google Gen AI SDK Gemma 4 client, structured prompt templates, grounded QA retrieval, anti-hallucination guardrails, test suites |

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines, branch conventions, and PR review standards.

---

## 📚 Documentation Index

- [Architecture & Data Flow](docs/architecture.md)
- [Gemma Model Integration](docs/gemma_integration.md)
- [Testing Guide & Matrix](docs/testing_guide.md)
- [Hackathon Live Demo Script](docs/demo_script.md)
- [Hackathon Submission Package](docs/submission.md)

---

## ⚠️ Known Limitations
- Initial Faster-Whisper model download requires an active internet connection; subsequent transcription runs completely offline.
- Large video files (>100MB) should be compressed or converted to audio before upload.
- Grounded Q&A requires speech clarity in the input audio; low SNR recordings may reduce transcript accuracy.

---

## 📄 License
This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
