"""
Phase 13 Competitive Benchmark v2 Test Suite.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.competitive_benchmark_v2 import CompetitiveBenchmarkV2

class TestCompetitiveBenchmarkV2:
    def test_benchmark_matrix_evaluation(self):
        matrix = CompetitiveBenchmarkV2.evaluate_all()
        assert "AI OS v4" in matrix
        assert "LangGraph" in matrix
        assert "CrewAI" in matrix
        assert matrix["AI OS v4"]["failure_tested"] is True
        assert matrix["AI OS v4"]["score_out_of_100"] == 98
