"""
Phase 11 Governance Control Plane Test Suite.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.governance_control_plane import GovernanceControlPlane

class TestGovernanceControlPlane:
    def test_low_risk_auto_approve(self):
        res = GovernanceControlPlane.evaluate_request("A06", "read_file", "data.json", "low")
        assert res["allowed"] is True
        assert res["approval_required"] is False
        assert res["audit_record"]["decision"] == "APPROVED"

    def test_high_risk_requires_human_approval(self):
        res = GovernanceControlPlane.evaluate_request("A10", "deploy_production", "cluster-1", "high")
        assert res["allowed"] is True
        assert res["approval_required"] is True
        assert res["audit_record"]["decision"] == "HUMAN_APPROVAL_NEEDED"

    def test_prohibited_action_rejected(self):
        res = GovernanceControlPlane.evaluate_request("A06", "DROP_DATABASE", "main_db", "critical")
        assert res["allowed"] is False
        assert res["audit_record"]["decision"] == "REJECTED"
