# Hackathon Live Demo Script (3 Minutes)

This script provides an engaging, concise walkthrough for presenting Live Transcript AI to hackathon judges.

---

## Preparation (Before Demo)
1. Ensure `.venv` is activated.
2. Launch Streamlit: `streamlit run app.py`.
3. Open browser to `http://localhost:8501`.
4. Ensure your free Gemini API key is entered in the left sidebar.

---

## Presentation Walkthrough

### Act 1: The Problem (0:00 - 0:40)
> *"Judges, students and developers consume hours of educational videos, tech talks, and lectures every week. But audio and video are locked media—you can\'t Ctrl+F audio, you can\'t easily search spoken ideas, and taking manual notes takes you out of the conversation. Our previous project focused on raw desktop audio capture, but for this hackathon, we built Live Transcript AI to turn spoken media into searchable, actionable knowledge powered by Google Gemma 4."*

### Act 2: Local Audio Transcription (0:40 - 1:20)
> *"Let\'s show you how it works live. We can upload any MP3, WAV, or video recording, or click 'Load Hackathon Sample' right here. When we hit 'Transcribe Audio', Faster-Whisper runs locally on the CPU using int8 quantization. Within seconds, it produces a high-accuracy, timestamped transcript without uploading audio anywhere, preserving privacy and eliminating bandwidth costs."*

### Act 3: Intelligent Learning Notes with Gemma 4 (1:20 - 2:00)
> *"Now for the magic. We click 'Generate Learning Notes with Gemma 4'. Using the Google Gen AI SDK, Gemma 4 analyzes the transcript and synthesizes an academic-grade study guide:
> - An executive summary of the core thesis
> - Categorized main topics
> - Key concepts and definitions
> - Concrete takeaways and real-world examples."*

### Act 4: Grounded Q&A and Zero Hallucination (2:00 - 2:40)
> *"Next, let\'s look at 'Ask the Transcript'. Often LLMs hallucinate information that was never in the lecture. With our grounded QA engine, Gemma 4 only answers questions using verified transcript evidence.
> - When we ask: 'What model powers the application?', Gemma correctly answers: 'Google Gemma 4' and shows the exact timestamped passage.
> - But when we ask an unanswerable question like: 'What is the capital of France?', Gemma strictly declines: 'Based on the provided transcript, there is insufficient evidence to answer this question.' Zero hallucinations."*

### Act 5: Multi-Format Export & Closing (2:40 - 3:00)
> *"Finally, students can export their work as plain TXT, beautifully formatted Markdown notes for Obsidian or Notion, or structured JSON for developer pipelines. Live Transcript AI brings together privacy-first local Whisper transcription and state-of-the-art Gemma 4 reasoning into one accessible tool. Thank you!"*
