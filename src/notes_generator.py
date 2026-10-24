"""AI Notes and Concept Generation Module using Gemma 4."""

from typing import Dict, List, Optional, Any
from src.gemma_client import GemmaClient


class NotesGenerator:
    """Generates structured summaries, key concepts, and learning notes from transcripts."""

    SYSTEM_PROMPT = (
        "You are an expert AI academic tutor and technical note-taker specializing in "
        "transforming raw spoken transcripts into clear, structured learning materials. "
        "Strict rules:\n"
        "1. Ground all notes exclusively in the provided transcript text.\n"
        "2. Do NOT invent quotations, external facts, or attribute unmade claims to the speaker.\n"
        "3. If the transcript is brief or lacks sufficient context, explicitly state that.\n"
        "4. Format the output with clear Markdown headers, bullet points, and callouts."
    )

    def __init__(self, gemma_client: Optional[GemmaClient] = None):
        self.client = gemma_client or GemmaClient()

    def generate_learning_notes(self, transcript_text: str) -> str:
        """Generate structured learning notes from the full transcript."""
        if not transcript_text or not transcript_text.strip():
            return "No transcript content available to generate notes."

        word_count = len(transcript_text.split())

        # If transcript is very short, adapt prompt appropriately
        if word_count < 15:
            prompt = (
                f"Transcript Content:\n\"\"\"{transcript_text}\"\"\"\n\n"
                "The transcript above is brief. Please provide:\n"
                "1. Brief Summary (1-2 sentences)\n"
                "2. Stated Intent or Key Phrase\n"
                "3. Note on brevity: acknowledge that the recording contains limited information."
            )
        else:
            prompt = (
                f"Transcript Content:\n\"\"\"{transcript_text}\"\"\"\n\n"
                "Analyze the transcript and produce high-quality learning notes formatted in Markdown:\n\n"
                "### 📌 Executive Summary\n"
                "A concise 2-3 sentence overview of the core message or topic.\n\n"
                "### 🎯 Main Topics Discussed\n"
                "Bulleted list of the primary subject matters covered.\n\n"
                "### 💡 Key Concepts & Terminology\n"
                "Define the most important technical concepts, frameworks, or terms mentioned in the text.\n\n"
                "### 📝 Key Takeaways & Details\n"
                "Important takeaways, arguments, or step-by-step points made by the speaker.\n\n"
                "### 🛠️ Practical Applications or Examples\n"
                "Any practical implementations, use-cases, or examples stated (or indicate if none were mentioned)."
            )

        return self.client.generate(prompt=prompt, system_instruction=self.SYSTEM_PROMPT, temperature=0.2)
