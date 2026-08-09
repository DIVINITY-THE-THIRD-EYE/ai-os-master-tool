"""
Deterministic Unit Tests for CapabilityBroker and ApprovalEngine.
Validates physical tool call denial by default and non-bypassable human approval tickets.
"""

import sys
from pathlib import Path
import pytest

# Ensure root directory is in sys.path
root_dir = Path(__file__).parent.parent.parent.resolve()
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from security.contracts import (
    AgentIdentity,
    CapabilityGrant,
    ToolCallRequest,
    RiskLevel,
    TrustLevel,
    ApprovalStatus
)
from execution.capability_broker import CapabilityBroker
from governance.approval_engine import ApprovalEngine


class TestCapabilityBrokerSecurity:
    def setup_method(self):
        self.approval_engine = ApprovalEngine()
        self.broker = CapabilityBroker(approval_engine=self.approval_engine)

        # Register Agent A06 with specific file_tool grant
        grant = CapabilityGrant(
            capability_id="tool_file",
            allowed_actions=["read_file", "write_file"],
            max_invocations=5
        )
        self.agent_a06 = AgentIdentity(
            agent_id="A06",
            name="Worker Execution Agent",
            trust_level=TrustLevel.STANDARD,
            grants=[grant]
        )
        self.broker.register_identity(self.agent_a06)

    def test_deny_by_default_unregistered_agent(self):
        req = ToolCallRequest(
            requester_id="UNKNOWN_AGENT",
            tool_name="tool_file",
            action="read_file",
            risk_level=RiskLevel.LOW
        )
        res = self.broker.authorize_tool_call(req)
        assert res.allowed is False
        assert "not registered" in res.reason

    def test_deny_by_default_ungranted_tool(self):
        req = ToolCallRequest(
            requester_id="A06",
            tool_name="tool_bash_execute",
            action="run_command",
            risk_level=RiskLevel.LOW
        )
        res = self.broker.authorize_tool_call(req)
        assert res.allowed is False
        assert "Denied by default" in res.reason

    def test_deny_by_default_ungranted_action(self):
        req = ToolCallRequest(
            requester_id="A06",
            tool_name="tool_file",
            action="delete_file",
            risk_level=RiskLevel.LOW
        )
        res = self.broker.authorize_tool_call(req)
        assert res.allowed is False
        assert "Denied by default" in res.reason

    def test_authorized_tool_call_success(self):
        req = ToolCallRequest(
            requester_id="A06",
            tool_name="tool_file",
            action="read_file",
            risk_level=RiskLevel.LOW
        )
        res = self.broker.authorize_tool_call(req)
        assert res.allowed is True
        assert "Authorized" in res.reason

    def test_high_risk_requires_approval_ticket(self):
        req = ToolCallRequest(
            requester_id="A06",
            tool_name="tool_file",
            action="write_file",
            risk_level=RiskLevel.HIGH
        )
        res = self.broker.authorize_tool_call(req)
        assert res.allowed is False
        assert res.requires_approval is True
        assert res.approval_ticket_id is not None

        # Approve ticket manually
        ticket_id = res.approval_ticket_id
        self.approval_engine.approve_ticket(ticket_id, approver_id="HUMAN_A13")

        # Re-attempt with approved ticket ID
        req_approved = ToolCallRequest(
            requester_id="A06",
            tool_name="tool_file",
            action="write_file",
            risk_level=RiskLevel.HIGH,
            approval_ticket_id=ticket_id
        )
        res_after = self.broker.authorize_tool_call(req_approved)
        assert res_after.allowed is True

    def test_revoked_agent_denied(self):
        self.broker.revoke_identity("A06")
        req = ToolCallRequest(
            requester_id="A06",
            tool_name="tool_file",
            action="read_file",
            risk_level=RiskLevel.LOW
        )
        res = self.broker.authorize_tool_call(req)
        assert res.allowed is False
        assert "revoked" in res.reason
