"""
AIOS Non-Bypassable Governance & Approval Ticket Engine.
Enforces mandatory Human-in-the-loop (A13) approval tickets for HIGH and CRITICAL risk operations.
"""

import uuid
from typing import Dict, Optional
from security.contracts import ApprovalTicket, ApprovalStatus, RiskLevel, ToolCallRequest

class ApprovalEngine:
    def __init__(self):
        self.tickets: Dict[str, ApprovalTicket] = {}

    def create_ticket(self, request: ToolCallRequest) -> ApprovalTicket:
        ticket_id = f"TICKET-{str(uuid.uuid4())[:8].upper()}"
        ticket = ApprovalTicket(
            ticket_id=ticket_id,
            requester_id=request.requester_id,
            action=request.action,
            parameters=request.parameters,
            risk_level=request.risk_level,
            status=ApprovalStatus.PENDING
        )
        self.tickets[ticket_id] = ticket
        return ticket

    def approve_ticket(self, ticket_id: str, approver_id: str, reason: str = "Approved by human authority") -> Optional[ApprovalTicket]:
        if ticket_id in self.tickets:
            ticket = self.tickets[ticket_id]
            ticket.status = ApprovalStatus.APPROVED
            ticket.approver_id = approver_id
            ticket.reason = reason
            return ticket
        return None

    def reject_ticket(self, ticket_id: str, approver_id: str, reason: str = "Rejected by human authority") -> Optional[ApprovalTicket]:
        if ticket_id in self.tickets:
            ticket = self.tickets[ticket_id]
            ticket.status = ApprovalStatus.REJECTED
            ticket.approver_id = approver_id
            ticket.reason = reason
            return ticket
        return None

    def is_ticket_approved(self, ticket_id: str) -> bool:
        ticket = self.tickets.get(ticket_id)
        return ticket is not None and ticket.status == ApprovalStatus.APPROVED
