---
name: "Task: Audio Validation & Faster-Whisper Transcription"
about: Track the implementation of audio upload, format validation, and local Whisper transcription.
title: "[FEAT] Local Audio Transcription Engine"
labels: ["enhancement", "lead-task"]
assignees: ["surya-devi06"]
---

### Objectives
- [x] Implement file validation for audio/video formats (.wav, .mp3, .m4a, .mp4, .webm) and size limits (100MB).
- [x] Configure Faster-Whisper to run with int8 quantization on CPU for low latency and zero API cost.
- [x] Extract timestamped segments, detected language, and duration metrics.
- [x] Handle missing, corrupted, or unsupported audio files gracefully.
