"""End-to-end automated integration tests for Live Transcript AI."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.transcriber import AudioTranscriber
from src.notes_generator import NotesGenerator
from src.qa_engine import QAEngine
from src.export_utils import ExportManager
from tests.test_notes_and_qa import MockGemmaClient


def test_full_workflow():
    print("\n" + "=" * 60)
    print("RUNNING END-TO-END WORKFLOW INTEGRATION TEST")
    print("=" * 60)

    # 1. Transcribe real speech
    audio_file = "samples/sample_speech.wav"
    assert os.path.exists(audio_file)

    transcriber = AudioTranscriber(model_size="tiny", device="cpu", compute_type="int8")
    result = transcriber.transcribe(audio_file)
    assert result.full_text != ""
    print(f"[OK] Step 1: Transcribed audio -> \"{result.full_text}\"")

    # 2. Notes Generation (using mock for deterministic CI/offline test)
    mock_client = MockGemmaClient()
    generator = NotesGenerator(gemma_client=mock_client)
    notes = generator.generate_learning_notes(result.full_text)
    assert notes != ""
    print(f"[OK] Step 2: Generated notes ({len(notes)} chars)")

    # 3. Grounded Question Answering
    qa_engine = QAEngine(gemma_client=mock_client)
    qa_res = qa_engine.answer_question(
        question="What model powers Live Transcript AI?",
        transcript_text=result.full_text,
        segments=result.segments,
    )
    assert qa_res["grounded"] is True
    print(f"[OK] Step 3: Grounded Answer -> \"{qa_res['answer']}\"")

    # 4. Unanswerable Question
    unanswerable_res = qa_engine.answer_question(
        question="What is the capital of France?",
        transcript_text=result.full_text,
        segments=result.segments,
    )
    assert unanswerable_res["grounded"] is False
    print(f"[OK] Step 4: Correctly rejected unanswerable query -> \"{unanswerable_res['answer']}\"")

    # 5. Export Generation
    txt = ExportManager.export_as_txt(result.full_text, result.format_timestamped())
    md = ExportManager.export_as_markdown("Test Lecture", notes, result.full_text)
    js = ExportManager.export_as_json(result.to_dict(), notes, [qa_res])

    assert len(txt) > 0
    assert len(md) > 0
    assert len(js) > 0
    print("[OK] Step 5: Successfully generated TXT, Markdown, and JSON export bundles.")

    print("\n[OK] Complete end-to-end integration verified successfully!")


if __name__ == "__main__":
    test_full_workflow()
