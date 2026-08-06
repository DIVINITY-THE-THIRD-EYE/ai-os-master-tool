"""
Google AI Studio Integration & Exporter Tool for AI OS v4.

Verifies Google AI Studio Gemini API Key connectivity and prints system
instructions and code snippets for Google AI Studio prompts.
"""

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
PROMPTS_FILE = BASE_DIR / "knowledge" / "google_ai_studio_prompts.json"


def test_gemini_connection() -> bool:
    """Test Gemini API Key connection from Google AI Studio."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("[INFO] GEMINI_API_KEY environment variable is not set.")
        print("       Set GEMINI_API_KEY in your .env file or terminal to test live AI Studio connections.\n")
        return False

    try:
        import google.generativeai as genai

        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-pro")
        res = model.generate_content("Ping AI OS Master Tool")
        print("[SUCCESS] Successfully connected to Google AI Studio Gemini API!")
        print(f"          Response snippet: {res.text[:60]}...\n")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to connect to Google AI Studio Gemini API: {e}\n")
        return False


def load_ai_studio_bundle() -> dict:
    """Load Google AI Studio JSON prompt bundle."""
    if PROMPTS_FILE.is_file():
        return json.loads(PROMPTS_FILE.read_text(encoding="utf-8"))
    return {}


def export_summary() -> None:
    """Print Google AI Studio agent system instructions."""
    bundle = load_ai_studio_bundle()
    print("=" * 60)
    print("AI OS v4 — Google AI Studio Agent Prompts Bundle")
    print("=" * 60)
    agents = bundle.get("agents", [])
    print(f"Total Agents Configured: {len(agents)}")
    print("-" * 60)
    for agent in agents:
        print(f"[{agent['agent_id']}] {agent['name']} -> Model: {agent['recommended_model']}")
        print(f"     System Instruction: {agent['system_instruction'][:90]}...")
        print()
    print("=" * 60)


if __name__ == "__main__":
    test_gemini_connection()
    export_summary()
