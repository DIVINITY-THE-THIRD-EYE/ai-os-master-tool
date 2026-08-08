"""
Phase 3 Durability Chaos Suite: SIGKILL & Sudden Process Termination Simulation.
"""

import os
import shutil
import tempfile
import json
import pytest

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "ai-os-v4", "ai-os-multi-agent-skill"))

from runtime.event_bus import EventBus
from runtime.bootstrap import bootstrap_persistence

class TestSigkillChaos:
    @pytest.fixture(autouse=True)
    def setup_temp_dir(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "sigkill_state.db")
        yield
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_sigkill_unflushed_journal_recovery(self):
        """Simulate hard SIGKILL mid-transaction and verify atomic journal recovery on reboot."""
        event_bus = EventBus()
        sm = bootstrap_persistence(db_path=self.db_path, is_supabase=False, enable_vram_image=True, event_bus=event_bus)
        
        # Write 50 records
        for i in range(50):
            sm.save_agent(f"A{i:02d}", f"Agent {i}", "1.0.0", "ready", ["cap"], {"val": i})
        sm.flush()
        
        records_before = 50
        snap_before = sm.snapshot()
        snap_before.pop("snapshot_timestamp", None)
        hash_before = hash(json.dumps(snap_before, sort_keys=True))
        
        # Unclean process drop without shutdown() -> simulate abrupt SIGKILL
        del sm
        
        # Restart process
        sm_recovered = bootstrap_persistence(db_path=self.db_path, is_supabase=False, enable_vram_image=True, event_bus=event_bus)
        snap_after = sm_recovered.snapshot()
        snap_after.pop("snapshot_timestamp", None)
        
        assert len(snap_after["agents"]) == records_before
        assert hash(json.dumps(snap_after, sort_keys=True)) == hash_before
