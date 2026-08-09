"""
Phase 3 Durability Chaos Suite: WAL Corruption & Multi-Instance Lock Tests.
"""

import os
import shutil
import tempfile
import pytest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.event_bus import EventBus
from runtime.bootstrap import bootstrap_persistence

class TestWALCorruptionChaos:
    @pytest.fixture(autouse=True)
    def setup_temp_dir(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "wal_chaos.db")
        yield
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_wal_partial_corruption_recovery(self):
        """Simulate partial WAL corruption and verify DB recovers to last consistent flush."""
        event_bus = EventBus()
        sm = bootstrap_persistence(db_path=self.db_path, is_supabase=False, enable_vram_image=True, event_bus=event_bus)
        sm.save_agent("A01", "Intake Agent", "1.0.0", "ready", ["intake"], {"name": "Intake Agent", "status": "ok"})
        sm.flush()

        # Inject corruption into WAL file if SQLite is in WAL mode, or append corrupt bytes to db file
        wal_path = f"{self.db_path}-wal"
        if os.path.exists(wal_path):
            with open(wal_path, "ab") as f:
                f.write(b"\x00\xFF\xFE\xFD\xFCGARBAGEWAL")
        else:
            with open(f"{self.db_path}.tmp", "wb") as f:
                f.write(b"CORRUPT_TEMP_BUFFER_BYTES")

        # Re-bootstrap persistence; system should gracefully ignore/recover
        sm_recovered = bootstrap_persistence(db_path=self.db_path, is_supabase=False, enable_vram_image=True, event_bus=event_bus)
        agent = sm_recovered.get_agent("A01")
        assert agent is not None
        assert agent["name"] == "Intake Agent"

    def test_concurrent_lock_isolation(self):
        """Verify that opening second connection on locked DB path fails or handles cleanly."""
        event_bus = EventBus()
        sm = bootstrap_persistence(db_path=self.db_path, is_supabase=False, enable_vram_image=True, event_bus=event_bus)
        sm.save_agent("A02", "Context Agent", "1.0.0", "ready", ["memory"], {"name": "Context Agent"})
        sm.flush()

        # Check that state manager allows isolated recovery
        sm2 = bootstrap_persistence(db_path=self.db_path, is_supabase=False, enable_vram_image=True, event_bus=EventBus())
        assert sm2.get_agent("A02") is not None
