"""
Phase 3 Durability Chaos Suite: Corrupted Snapshot Recovery.
"""

import os
import shutil
import tempfile
import pytest

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "ai-os-v4", "ai-os-multi-agent-skill"))

from runtime.event_bus import EventBus
from runtime.bootstrap import bootstrap_persistence

class TestCorruptSnapshotChaos:
    @pytest.fixture(autouse=True)
    def setup_temp_dir(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "corrupt_state.db")
        yield
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_corrupt_tmp_file_fallback(self):
        """Simulate a crash leaving a corrupt .tmp file and prove DB recovers cleanly."""
        event_bus = EventBus()
        sm = bootstrap_persistence(db_path=self.db_path, is_supabase=False, enable_vram_image=True, event_bus=event_bus)
        sm.save_agent("A01", "Intake Agent", "1.0.0", "ready", ["intake"], {"key": "val"})
        sm.flush()
        
        # Inject corrupted temp snapshot
        corrupt_tmp = f"{self.db_path}.tmp"
        with open(corrupt_tmp, "w") as f:
            f.write("GARBAGE DATA NOISE 0xBADF00D")

        # Restart process
        sm_recovered = bootstrap_persistence(db_path=self.db_path, is_supabase=False, enable_vram_image=True, event_bus=event_bus)
        agent = sm_recovered.get_agent("A01")
        assert agent is not None
        assert agent["key"] == "val"
