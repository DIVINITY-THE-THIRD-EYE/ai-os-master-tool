"""
AIOS Capability Broker — Programmatic, code-enforced, deny-by-default tool call interceptor.
Physical security broker ensuring no tool call can execute without valid grants and required approvals.
"""

from typing import Dict, Optional
from security.contracts import (
    AgentIdentity,
    ToolCallRequest,
    CapabilityBrokerResult,
    RiskLevel
)
from governance.approval_engine import ApprovalEngine

class CapabilityBroker:
    """
    Physical security barrier. Intercepts tool calls prior to execution.
    Denies by default.
    """

    def __init__(self, approval_engine: Optional[ApprovalEngine] = None):
        self.identities: Dict[str, AgentIdentity] = {}
        self.approval_engine = approval_engine or ApprovalEngine()

    def register_identity(self, identity: AgentIdentity) -> None:
        self.identities[identity.agent_id] = identity

    def revoke_identity(self, agent_id: str) -> None:
        if agent_id in self.identities:
            self.identities[agent_id].revoked = True

    def authorize_tool_call(self, request: ToolCallRequest) -> CapabilityBrokerResult:
        # 1. Identity Check
        identity = self.identities.get(request.requester_id)
        if not identity:
            return CapabilityBrokerResult(
                allowed=False,
                reason=f"Security Denial: Requester '{request.requester_id}' is not registered."
            )

        if identity.revoked:
            return CapabilityBrokerResult(
                allowed=False,
                reason=f"Security Denial: Agent '{request.requester_id}' identity has been revoked."
            )

        # 2. Risk & Approval Ticket Enforcement
        if request.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            if not request.approval_ticket_id:
                ticket = self.approval_engine.create_ticket(request)
                return CapabilityBrokerResult(
                    allowed=False,
                    reason=f"Security Hold: {request.risk_level.value} risk action requires human approval ticket.",
                    requires_approval=True,
                    approval_ticket_id=ticket.ticket_id
                )
            elif not self.approval_engine.is_ticket_approved(request.approval_ticket_id):
                return CapabilityBrokerResult(
                    allowed=False,
                    reason=f"Security Denial: Approval ticket '{request.approval_ticket_id}' is not approved.",
                    requires_approval=True,
                    approval_ticket_id=request.approval_ticket_id
                )

        # 3. Capability Grant Matching (Deny-by-default)
        for grant in identity.grants:
            if grant.capability_id == request.tool_name or grant.capability_id == "*":
                if request.action in grant.allowed_actions or "*" in grant.allowed_actions:
                    if grant.max_invocations is not None and grant.invocation_count >= grant.max_invocations:
                        return CapabilityBrokerResult(
                            allowed=False,
                            reason=f"Security Denial: Capability '{grant.capability_id}' exceeded max invocation limit ({grant.max_invocations})."
                        )
                    
                    grant.invocation_count += 1
                    return CapabilityBrokerResult(
                        allowed=True,
                        reason="Authorized: Matching capability grant verified."
                    )

        return CapabilityBrokerResult(
            allowed=False,
            reason=f"Security Denial: Denied by default. Requester '{request.requester_id}' lacks capability grant for tool '{request.tool_name}' and action '{request.action}'."
        )
