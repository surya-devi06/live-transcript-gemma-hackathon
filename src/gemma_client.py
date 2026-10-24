"""Gemma client module for Google Gemini API integration."""

import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class GemmaClient:
    """Client for interacting with Google Gemma open-weight models via Gemini API."""

    SUPPORTED_GEMMA_MODELS = [
        "gemma-4-26b-a4b-it",
        "gemma-3-27b-it",
        "gemma-3-12b-it",
        "gemma-3-4b-it",
        "gemma-3-1b-it",
        "gemma-2-27b-it",
        "gemma-2-9b-it",
        "gemma-2-2b-it",
    ]

    def __init__(self, api_key: Optional[str] = None, model_id: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.model_id = model_id or os.getenv("GEMMA_MODEL_ID") or "gemma-4-26b-a4b-it"
        self._client = None

    def is_configured(self) -> bool:
        """Check if an API key is configured without exposing it."""
        return bool(self.api_key and self.api_key.strip() and not self.api_key.startswith("your_"))

    def get_client(self):
        """Initialize and return the Google GenAI client."""
        if not self.is_configured():
            raise ValueError(
                "Gemini API key is not configured. Please set GEMINI_API_KEY in your .env file."
            )
        if self._client is None:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def list_available_gemma_models(self) -> List[Dict[str, Any]]:
        """Query Gemini API for available Gemma models."""
        client = self.get_client()
        gemma_models = []
        try:
            for m in client.models.list():
                model_name = getattr(m, "name", "") or ""
                # Strip models/ prefix if present
                clean_name = model_name.replace("models/", "")
                if "gemma" in clean_name.lower():
                    gemma_models.append({
                        "name": clean_name,
                        "display_name": getattr(m, "display_name", clean_name),
                        "description": getattr(m, "description", ""),
                    })
        except Exception as e:
            raise RuntimeError(f"Failed to query model catalog from Gemini API: {e}")
        return gemma_models

    def generate(self, prompt: str, system_instruction: Optional[str] = None, temperature: float = 0.2) -> str:
        """Generate text using the configured Gemma model."""
        client = self.get_client()
        from google.genai import types

        config = types.GenerateContentConfig(
            temperature=temperature,
        )
        if system_instruction:
            config.system_instruction = system_instruction

        response = client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=config,
        )
        return response.text or ""
