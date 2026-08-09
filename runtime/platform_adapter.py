"""
AI OS Platform Adapter Engine — translates universal system rules, policies, and prompts into host-specific instruction artifacts.

Supported Targets:
- CLAUDE (Anthropic XML tag formatting and strict system prompt guidelines)
- CHATGPT (OpenAI System / Developer role formatting)
- GEMINI (Google System Instruction structure)
- CURSOR_ANTIGRAVITY (Antigravity skill & markdown rule formatting)
- GENERIC (Standard markdown instruction format)
"""

from enum import Enum
from typing import Dict, Any, Optional

class TargetPlatform(Enum):
    CLAUDE = "claude"
    CHATGPT = "chatgpt"
    GEMINI = "gemini"
    CURSOR_ANTIGRAVITY = "cursor_antigravity"
    GENERIC = "generic"

class PlatformAdapter:
    @staticmethod
    def adapt_instructions(universal_prompt: str, target_platform: str) -> str:
        try:
            target = TargetPlatform(target_platform.lower())
        except ValueError:
            target = TargetPlatform.GENERIC

        if target == TargetPlatform.CLAUDE:
            return f"<system_instructions>\n{universal_prompt.strip()}\n</system_instructions>\n<formatting_rule>Use clean XML tags and markdown blocks.</formatting_rule>"

        if target == TargetPlatform.CHATGPT:
            return f"[SYSTEM DEVELOPER DIRECTIVE]\n{universal_prompt.strip()}\n\n[FORMATTING] Respond with clear structured markdown sections."

        if target == TargetPlatform.GEMINI:
            return f"=== GEMINI SYSTEM INSTRUCTION ===\n{universal_prompt.strip()}\n\nEnsure responses follow Google AI guidelines."

        if target == TargetPlatform.CURSOR_ANTIGRAVITY:
            return f"# ANTIGRAVITY INSTRUCTION PACKAGE\n\n{universal_prompt.strip()}\n\n> Always follow .agents/rules/ constraints."

        return f"# UNIVERSAL INSTRUCTIONS\n\n{universal_prompt.strip()}"
