"""
Strict type contracts for AIOS Security, Identity, Capabilities, and Governance.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class TrustLevel(str, Enum):
    UNTRUSTED = "UNTRUSTED"
    STANDARD = "STANDARD"
    ELEVATED = "ELEVATED"
    SYSTEM = "SYSTEM"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class CapabilityGrant(BaseModel):
    capability_id: str
    allowed_actions: List[str] = Field(default_factory=list)
    resource_patterns: List[str] = Field(default_factory=list)
    max_invocations: Optional[int] = None
    invocation_count: int = 0


class AgentIdentity(BaseModel):
    agent_id: str
    name: str
    trust_level: TrustLevel = TrustLevel.STANDARD
    grants: List[CapabilityGrant] = Field(default_factory=list)
    revoked: bool = False
    parent_agent_id: Optional[str] = None


class ToolCallRequest(BaseModel):
    requester_id: str
    tool_name: str
    action: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    risk_level: RiskLevel = RiskLevel.LOW
    approval_ticket_id: Optional[str] = None


class CapabilityBrokerResult(BaseModel):
    allowed: bool
    reason: str
    requires_approval: bool = False
    approval_ticket_id: Optional[str] = None


class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ApprovalTicket(BaseModel):
    ticket_id: str
    requester_id: str
    action: str
    parameters: Dict[str, Any]
    risk_level: RiskLevel
    status: ApprovalStatus = ApprovalStatus.PENDING
    approver_id: Optional[str] = None
    reason: Optional[str] = None
