# Hackathon Submission Package

## 1. Project Overview
- **Project Name**: Live Transcript AI — Powered by Gemma
- **Tagline**: Turn spoken content into searchable transcripts, intelligent notes, and interactive learning.
- **Repository**: `https://github.com/surya-devi06/live-transcript-gemma-hackathon` (and backup: `https://github.com/surya-devi06/Live-Transcript-AI-Gemma-4-Hackathon-Project`)
- **Hackathon Event**: Otaku.dev '26 — Hacktoberfest Hack Day, Chennai
- **Target Categories**:
  - *Best Use of Gemma 4*
  - *Best Open-Source AI Project*

---

## 2. Problem Statement
Audio and video content are inherently linear and locked:
- Students and professionals spend hours re-watching lectures and talks to find specific information.
- Manual note-taking distracts from active listening.
- Generic cloud speech APIs introduce recurring costs, latency, and privacy risks when sensitive meeting recordings are uploaded.
- Standard generative AI often hallucinates when asked about specific lectures, introducing false claims.

---

## 3. The Solution
Live Transcript AI provides a privacy-first, edge-assisted solution:
1. **On-Device Speech-to-Text**: Faster-Whisper transcribes speech locally in seconds using CPU int8 quantization—zero audio data leaves the machine.
2. **Cognitive Synthesis via Google Gemma 4**: Using the official Google Gen AI SDK, Gemma 4 extracts executive summaries, core concepts, and structured study notes.
3. **Anti-Hallucination Grounded Q&A**: Users can interrogate the transcript; Gemma strictly answers with timestamp citations and declines out-of-scope questions.
4. **Export Readiness**: Instantly download Markdown notes, timestamped text transcripts, or raw JSON bundles.

---

## 4. Technology Stack
- **Frontend**: Streamlit
- **Transcription**: Faster-Whisper (CTranslate2 backend)
- **AI / LLM**: Google Gemma 4 (`gemma-4-26b-a4b-it`) via `google-genai` SDK
- **Language & Runtime**: Python 3.10+
- **Configuration**: python-dotenv
- **Testing**: Pytest & Python unittest

---

## 5. Verified Features vs. Known Limitations

### Verified & Tested Features:
- [x] Multi-format audio validation and ingestion (.wav, .mp3, .m4a, .mp4, .webm).
- [x] Local speech-to-text with Faster-Whisper and timestamp generation.
- [x] Google Gen AI SDK client setup and model variant selection.
- [x] Structured note generation and executive summary synthesis with Gemma 4.
- [x] Grounded Q&A with lexical evidence retrieval and refusal for unanswerable questions.
- [x] Multi-format export (TXT, Markdown, JSON).
- [x] Full offline end-to-end integration test suite passing.

### Known Limitations:
- Very long multi-hour lectures may require batching or chunked summarization if transcript exceeds token window.
- First model download for Whisper requires an initial internet connection; subsequent runs are 100% offline.
- Gemma inference requires an active Google AI Studio / Gemini API key with network access.

---

## 6. Team Contributions
- **Surya (Project Lead)**:
  - Architecture design and separate hackathon repository setup.
  - Local Faster-Whisper transcription integration and audio preprocessing.
  - Streamlit UI development and multi-format export manager.
  - System integration, end-to-end testing, and submission documentation.
- **Teammate (AI & Quality)**:
  - Google Gen AI SDK client and Gemma 4 model integration.
  - Prompt engineering for structured notes and executive summaries.
  - Grounded Q&A engine with lexical retrieval and anti-hallucination guardrails.
  - Test suite design (`test_transcription.py`, `test_notes_and_qa.py`) and verification checklist.
