"""
Phase 11 Platform Adapter Test Suite.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.platform_adapter import PlatformAdapter, TargetPlatform

class TestPlatformAdapter:
    def test_claude_adaptation(self):
        adapted = PlatformAdapter.adapt_instructions("You are A01.", "claude")
        assert "<system_instructions>" in adapted
        assert "You are A01." in adapted

    def test_chatgpt_adaptation(self):
        adapted = PlatformAdapter.adapt_instructions("You are A01.", "chatgpt")
        assert "[SYSTEM DEVELOPER DIRECTIVE]" in adapted

    def test_gemini_adaptation(self):
        adapted = PlatformAdapter.adapt_instructions("You are A01.", "gemini")
        assert "GEMINI SYSTEM INSTRUCTION" in adapted

    def test_antigravity_adaptation(self):
        adapted = PlatformAdapter.adapt_instructions("You are A01.", "cursor_antigravity")
        assert "ANTIGRAVITY INSTRUCTION PACKAGE" in adapted

    def test_generic_fallback(self):
        adapted = PlatformAdapter.adapt_instructions("You are A01.", "unknown_host")
        assert "# UNIVERSAL INSTRUCTIONS" in adapted
