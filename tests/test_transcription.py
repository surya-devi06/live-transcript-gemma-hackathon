"""Unit and integration test for AudioTranscriber using Faster-Whisper."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.transcriber import AudioTranscriber, TranscriptionResult


def test_validation_unsupported_file():
    transcriber = AudioTranscriber()
    # Create temporary dummy txt file
    dummy_path = "samples/test_dummy.txt"
    with open(dummy_path, "w") as f:
        f.write("not an audio")
    try:
        valid, err = transcriber.validate_file(dummy_path)
        assert not valid
        assert "Unsupported format" in err
    finally:
        if os.path.exists(dummy_path):
            os.remove(dummy_path)


def test_validation_missing_file():
    transcriber = AudioTranscriber()
    valid, err = transcriber.validate_file("samples/non_existent.wav")
    assert not valid
    assert "File not found" in err


def test_transcription_real_speech():
    sample_path = "samples/sample_speech.wav"
    assert os.path.exists(sample_path), "Sample speech file must exist"

    transcriber = AudioTranscriber(model_size="tiny", device="cpu", compute_type="int8")
    result = transcriber.transcribe(sample_path)

    print("\n" + "=" * 50)
    print("TRANSCRIPTION TEST OUTPUT")
    print("=" * 50)
    print(f"Detected Language: {result.detected_language}")
    print(f"Duration: {result.duration}s")
    print(f"Full Text: {result.full_text}")
    print("Timestamped Transcript:")
    print(result.format_timestamped())
    print("=" * 50)

    assert result.full_text != "", "Transcription should produce non-empty text"
    assert len(result.segments) > 0, "Segments should not be empty"
    assert result.detected_language in ["en", "nn"], "Language should be detected as English"
    assert "transcript" in result.full_text.lower() or "welcome" in result.full_text.lower(), (
        f"Expected spoken words in transcript, got: {result.full_text}"
    )


if __name__ == "__main__":
    test_validation_unsupported_file()
    test_validation_missing_file()
    test_transcription_real_speech()
    print("[OK] All Stage 4 Transcription tests passed successfully!")
