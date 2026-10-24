"""Audio and video transcription module using Faster-Whisper."""

import os
import tempfile
import time
from typing import Dict, List, Optional, Any, Tuple
from faster_whisper import WhisperModel


class TranscriptionResult:
    """Structured container for transcription output."""

    def __init__(
        self,
        full_text: str,
        segments: List[Dict[str, Any]],
        detected_language: str,
        duration: float,
        model_name: str,
    ):
        self.full_text = full_text
        self.segments = segments
        self.detected_language = detected_language
        self.duration = duration
        self.model_name = model_name

    def format_timestamped(self) -> str:
        """Format transcript with readable timestamps [MM:SS - MM:SS]."""
        lines = []
        for s in self.segments:
            start_m, start_s = divmod(int(s["start"]), 60)
            end_m, end_s = divmod(int(s["end"]), 60)
            lines.append(f"[{start_m:02d}:{start_s:02d} -> {end_m:02d}:{end_s:02d}] {s['text'].strip()}")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary representation."""
        return {
            "full_text": self.full_text,
            "segments": self.segments,
            "detected_language": self.detected_language,
            "duration": self.duration,
            "model_name": self.model_name,
        }


class AudioTranscriber:
    """Manages audio transcription via Faster-Whisper."""

    SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".mp4", ".webm", ".ogg"}
    MAX_FILE_SIZE_MB = 100

    def __init__(self, model_size: str = "tiny", device: str = "cpu", compute_type: str = "int8"):
        """Initialize transcription model configuration."""
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self._model: Optional[WhisperModel] = None

    def get_model(self) -> WhisperModel:
        """Lazy loader for the Whisper model to avoid unnecessary reloads."""
        if self._model is None:
            # Download/load model safely with int8 quantization on CPU
            self._model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
            )
        return self._model

    def validate_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """Validate input file format, existence, and size."""
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            return False, f"Unsupported format '{ext}'. Supported: {', '.join(sorted(self.SUPPORTED_EXTENSIONS))}"

        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > self.MAX_FILE_SIZE_MB:
            return False, f"File size ({size_mb:.1f} MB) exceeds maximum limit of {self.MAX_FILE_SIZE_MB} MB."

        if os.path.getsize(file_path) == 0:
            return False, "File is empty (0 bytes)."

        return True, None

    def transcribe(self, audio_path: str) -> TranscriptionResult:
        """Transcribe an audio or video file and return structured results."""
        is_valid, error_msg = self.validate_file(audio_path)
        if not is_valid:
            raise ValueError(error_msg)

        start_time = time.time()
        model = self.get_model()

        try:
            segments_generator, info = model.transcribe(
                audio_path,
                beam_size=5,
                vad_filter=True,  # Voice activity detection to skip silence
                vad_parameters=dict(min_silence_duration_ms=500),
            )

            segments_list = []
            text_parts = []

            for seg in segments_generator:
                cleaned_text = seg.text.strip()
                if cleaned_text:
                    segments_list.append({
                        "start": round(seg.start, 2),
                        "end": round(seg.end, 2),
                        "text": cleaned_text,
                    })
                    text_parts.append(cleaned_text)

            full_text = " ".join(text_parts).strip()
            duration = round(time.time() - start_time, 2)

            return TranscriptionResult(
                full_text=full_text,
                segments=segments_list,
                detected_language=info.language,
                duration=duration,
                model_name=f"faster-whisper-{self.model_size}",
            )
        except Exception as e:
            raise RuntimeError(f"Transcription failed: {str(e)}")
