# Architecture & Technical Design

## 1. Overview
Live Transcript AI transforms spoken lecture and meeting recordings into structured transcripts, educational summaries, and grounded Q&A using a hybrid edge-and-cloud architecture:
- **Speech-to-Text (Edge/Local)**: Faster-Whisper performs private, on-device audio transcription without sending raw audio across the network.
- **Reasoning & Summarization (Cloud LLM)**: Google Gemma 4 (via Google Gen AI SDK) generates hierarchical study notes and handles interactive grounded transcript Q&A.

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

## 2. Key Components

### 2.1 Audio Transcription (`src/transcriber.py`)
- **Engine**: Faster-Whisper (`WhisperModel`) running locally with int8 quantization on CPU for low latency and zero API cost.
- **Validation**: Checks file formats (`.mp3`, `.wav`, `.m4a`, `.mp4`, `.webm`, `.ogg`), rejects 0-byte files, and enforces a 100MB limit.
- **Voice Activity Detection**: Built-in Silero VAD filters out silence segments to speed up inference and improve timestamp accuracy.

### 2.2 Gemma Client (`src/gemma_client.py`)
- **SDK**: `google-genai` (Google Gen AI SDK v1+).
- **Target Model**: `gemma-4-26b-a4b-it` (Google Gemma 4).
- **Fallbacks**: Supports `gemma-3-27b-it`, `gemma-3-12b-it`, `gemma-2-27b-it` if required by quota or environment availability.
- **Safe Initialization**: Lazy loads credentials without leaking keys to logs or UI.

### 2.3 Notes Generator (`src/notes_generator.py`)
- Takes raw transcript text and prompts Gemma with an academic note-taker persona.
- Produces five distinct sections:
  1. Executive Summary
  2. Main Topics Discussed
  3. Key Concepts & Terminology
  4. Key Takeaways & Details
  5. Practical Applications & Examples

### 2.4 Grounded Q&A Engine (`src/qa_engine.py`)
- **Anti-Hallucination Guardrail**: Instructs the model to answer strictly and exclusively based on the transcript text. If evidence is lacking, it explicitly responds with "insufficient evidence".
- **Evidence Retrieval**: Ranks transcript segments by keyword relevance and surfaces exact timestamped citations.

### 2.5 Export Manager (`src/export_utils.py`)
- Generates clean, ready-to-use artifacts in three formats:
  - `.txt`: Formatted timestamped and raw transcript text.
  - `.md`: Markdown study guide with session details, notes, and transcript quote blocks.
  - `.json`: Machine-readable structured payload containing metadata, segments, notes, and QA history.
