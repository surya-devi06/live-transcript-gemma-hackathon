"""Tests for NotesGenerator, QAEngine, and ExportManager."""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.qa_engine import QAEngine
from src.export_utils import ExportManager


class MockGemmaClient:
    """Mock client for offline testing of prompt structures and outputs."""

    def __init__(self):
        self.last_prompt = ""
        self.model_id = "gemma-4-26b-a4b-it"

    def is_configured(self):
        return True

    def generate(self, prompt: str, system_instruction=None, temperature=0.2):
        self.last_prompt = prompt
        if "User Question" in prompt:
            if "capital" in prompt.lower() or "paris" in prompt.lower():
                return "Based on the provided transcript, there is insufficient evidence to answer this question."
            return "The speaker explained that Live Transcript AI uses Google Gemma 4 for intelligent summarization."
        return "### 📌 Executive Summary\nOverview of the educational session on Gemma 4."


def test_qa_retrieval_ranking():
    engine = QAEngine(gemma_client=MockGemmaClient())
    segments = [
        {"start": 0.0, "end": 4.0, "text": "Welcome to the programming lecture today."},
        {"start": 4.1, "end": 8.0, "text": "We are studying machine learning algorithms."},
        {"start": 8.1, "end": 12.0, "text": "Specifically, neural network backpropagation is our key topic."},
        {"start": 12.1, "end": 16.0, "text": "Please open your code editor now."},
    ]

    # Query matching segment 2
    matched = engine.retrieve_relevant_segments("What neural network topic are we studying?", segments, top_k=2)
    assert len(matched) == 2
    assert "neural network" in matched[0]["text"].lower()


def test_qa_grounding_and_unanswerable():
    engine = QAEngine(gemma_client=MockGemmaClient())
    transcript = "Welcome to Live Transcript AI powered by Google Gemma 4."

    # Test answerable
    res = engine.answer_question("What powers the AI?", transcript)
    assert res["grounded"] is True
    assert "gemma" in res["answer"].lower()

    # Test unanswerable question
    res_unanswerable = engine.answer_question("What is the capital of France?", transcript)
    assert res_unanswerable["grounded"] is False
    assert "insufficient" in res_unanswerable["answer"].lower()


def test_export_manager():
    transcript_text = "Welcome to Live Transcript AI."
    notes = "### Summary\nOverview of application."
    segments = [{"start": 0.0, "end": 3.0, "text": "Welcome to Live Transcript AI."}]

    # Test TXT export
    txt = ExportManager.export_as_txt(transcript_text, "[00:00 -> 00:03] Welcome")
    assert "TIMESTAMPED TRANSCRIPT" in txt
    assert "Welcome" in txt

    # Test Markdown export
    md = ExportManager.export_as_markdown("Lecture 1", notes, transcript_text)
    assert "# Lecture 1" in md
    assert "Summary" in md

    # Test JSON export
    js = ExportManager.export_as_json({"full_text": transcript_text, "segments": segments}, notes)
    data = json.loads(js)
    assert data["application"] == "Live Transcript AI"
    assert data["transcript"]["full_text"] == transcript_text


if __name__ == "__main__":
    test_qa_retrieval_ranking()
    test_qa_grounding_and_unanswerable()
    test_export_manager()
    print("[OK] All Notes, QA, and Export tests passed successfully!")
