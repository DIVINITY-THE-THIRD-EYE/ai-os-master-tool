"""
AI OS Security & Governance Control Plane Engine.

Decision Request -> Risk Classification -> Policy Evaluation -> Security Check -> Approval Required (Human vs Automatic) -> Execution Record.
"""

from typing import Dict, Any, Tuple

class GovernanceControlPlane:
    @staticmethod
    def evaluate_request(
        requester_agent_id: str,
        action: str,
        target_resource: str,
        risk_level: str
    ) -> Dict[str, Any]:
        risk_level_upper = risk_level.upper()
        approval_required = risk_level_upper in ["HIGH", "CRITICAL"]
        
        allowed = True
        reason = "Policy allowed action"
        
        if action == "DROP_DATABASE" or target_resource == "/etc/shadow":
            allowed = False
            reason = "Security policy violation: Prohibited system mutation"
            
        decision = "REJECTED" if not allowed else ("HUMAN_APPROVAL_NEEDED" if approval_required else "APPROVED")
        return {
            "requester_agent_id": requester_agent_id,
            "action": action,
            "target_resource": target_resource,
            "risk_classification": risk_level_upper,
            "allowed": allowed,
            "approval_required": approval_required,
            "reason": reason,
            "audit_record": {
                "who": requester_agent_id,
                "action": action,
                "risk": risk_level_upper,
                "decision": decision
            }
        }
