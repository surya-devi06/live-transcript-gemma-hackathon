"""Verification script for Gemma model connectivity via Gemini API."""

import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.gemma_client import GemmaClient


def verify_gemma_connectivity():
    print("=" * 60)
    print("STAGE 3: GEMMA MODEL CONNECTIVITY VERIFICATION")
    print("=" * 60)

    client = GemmaClient()

    # Step 1: Check API key configuration safely
    is_configured = client.is_configured()
    print(f"[1] API Key Configured: {'YES (Ready)' if is_configured else 'NO (Missing or placeholder)'}")

    if not is_configured:
        print("\n[!] Blocker: GEMINI_API_KEY is not set in .env")
        print("    Troubleshooting steps:")
        print("    1. Create a .env file: copy .env.example .env")
        print("    2. Get a free API key from https://aistudio.google.com/")
        print("    3. Add: GEMINI_API_KEY=AIzaSy...")
        return False, "API key not configured"

    # Step 2: Query available Gemma models
    print("\n[2] Discovering Gemma models available to this API key...")
    try:
        available_models = client.list_available_gemma_models()
        if available_models:
            print(f"    Found {len(available_models)} Gemma model(s):")
            for m in available_models:
                print(f"      - {m['name']} ({m.get('display_name', '')})")
        else:
            print("    [!] Warning: Model listing returned no models containing 'gemma'.")
            print("    Checking predefined supported models...")
    except Exception as e:
        print(f"    [!] Error during model catalog discovery: {e}")
        return False, f"Model discovery error: {e}"

    # Step 3: Minimal test request
    print(f"\n[3] Testing minimal prompt with target model: {client.model_id}...")
    test_prompt = "Hello! Please reply in one short sentence confirming that Gemma is working."
    try:
        reply = client.generate(test_prompt)
        print("    [✓] Model Response Received Successfully:")
        print(f"    \"{reply.strip()}\"")
        print("\n[✓] Stage 3 Passed: Gemma 4 API connectivity verified successfully!")
        return True, client.model_id
    except Exception as e:
        print(f"\n    [✗] Model Request Failed for '{client.model_id}': {e}")
        print("\n    Troubleshooting steps:")
        print("    1. Verify if the model ID is active on your Google AI Studio account.")
        print("    2. Check if your API key has quota or permissions for Gemma models.")
        print("    3. If 'gemma-4-26b-a4b-it' is not yet enabled, consider 'gemma-3-27b-it' or 'gemma-2-27b-it' with mentor approval.")
        return False, str(e)


if __name__ == "__main__":
    success, details = verify_gemma_connectivity()
    sys.exit(0 if success else 1)
