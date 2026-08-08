"""
Phase 9 Prompt Compiler Test Suite.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.prompt_compiler import PromptCompiler

class TestPromptCompiler:
    def test_prompt_compilation_and_validation(self):
        compiled = PromptCompiler.compile_prompt(
            base_prompt="You are A01 Intake Agent.",
            task_description="Parse user requirements for payment API.",
            domain_rules=["Must comply with PCI-DSS", "No plain text tokens"],
            security_policy="Zero secrets in prompt or log",
            tools=["tool_file_read"],
            quality_gates={"min_quality_score": 0.85}
        )
        
        assert "A01 Intake Agent" in compiled
        assert "PCI-DSS" in compiled
        assert "Zero secrets" in compiled
        assert "min_quality_score" in compiled
