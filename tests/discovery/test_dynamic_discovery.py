"""
Phase 7 Dynamic Discovery Test Suite.
Verifies dynamic loading and capability matching from registry/agents.yaml.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.agent_registry import AgentRegistry, AgentRecord
from runtime.capability_router import CapabilityRouter
from runtime.master_registry import MasterRegistry

class TestDynamicDiscovery:
    def test_dynamic_registry_discovery_and_routing(self):
        """Load agents dynamically from master registry and verify routing capability matching."""
        status = MasterRegistry.get_status()
        agents_data = status.get("agents", {}).get("agents", [])
        
        registry = AgentRegistry()
        for a in agents_data:
            rec = AgentRecord(
                agent_id=a["id"],
                name=a["name"],
                version="1.0.0",
                capabilities=[f"cap_{a['id']}"],
                skills=[],
                tools=[],
                permissions=[]
            )
            registry.register(rec)
            registry.configure(a["id"])
            registry.mark_ready(a["id"])

        router = CapabilityRouter(registry)
        selected = router.route("cap_A01", "task-dyn", "trace-dyn")
        assert selected is not None
        assert selected.agent_id == "A01"
        assert selected.name == "Intake Agent"

    def test_master_registry_find_agent_by_id(self):
        """Verify direct agent lookup via MasterRegistry discovery helper."""
        a00 = MasterRegistry.find_agent_by_id("A00")
        assert a00 is not None
        assert a00["name"] == "Master Orchestrator"

        a01 = MasterRegistry.find_agent_by_id("A01")
        assert a01 is not None
        assert a01["name"] == "Intake Agent"
