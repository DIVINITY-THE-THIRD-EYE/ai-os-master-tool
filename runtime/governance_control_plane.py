"""
AI OS Security & Governance Control Plane Engine.

Decision Request -> Risk Classification -> Policy Evaluation -> Security Check -> Approval Required (Human vs Automatic) -> Execution Record.
Includes Prompt Injection Guardrails, Memory Poisoning Protection, and Delegation Narrowing.
"""

import re
from typing import Dict, Any, Tuple, List, Optional

TRUST_LEVEL_HIERARCHY = {
    "UNTRUSTED": 0,
    "STANDARD": 1,
    "ELEVATED": 2,
    "SYSTEM": 3
}

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"disregard\s+(all\s+)?prior\s+system",
    r"system\s+override",
    r"you\s+are\s+now\s+a\s+DAN",
    r"bypass\s+security\s+policy"
]

RESERVED_MEMORY_KEYS = [
    "system_metadata",
    "security_policy",
    "master_key",
    "root_credentials"
]

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

    @staticmethod
    def validate_prompt_injection(prompt: str) -> Tuple[bool, Optional[str]]:
        """Detect prompt injection or jailbreak attempts in inputs."""
        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, prompt, re.IGNORECASE):
                return False, f"Prompt injection pattern detected: '{pattern}'"
        return True, None

    @staticmethod
    def sanitize_memory_input(key: str, value: Any) -> Tuple[bool, Optional[str]]:
        """Sanitize memory writes to prevent memory poisoning and reserved key overwrite."""
        if key in RESERVED_MEMORY_KEYS:
            return False, f"Memory poisoning attempt: Cannot overwrite reserved system key '{key}'"
        if isinstance(value, str) and ("<script>" in value or "eval(" in value):
            return False, "Memory poisoning attempt: Malicious script/payload detected in memory value"
        return True, None

    @staticmethod
    def validate_delegation(
        parent_agent_id: str,
        child_agent_id: str,
        parent_trust: str,
        child_trust: str,
        revocation_list: Optional[List[str]] = None
    ) -> Tuple[bool, Optional[str]]:
        """Enforce delegation narrowing: child trust level cannot exceed parent trust level."""
        revocation_list = revocation_list or []
        if parent_agent_id in revocation_list or child_agent_id in revocation_list:
            return False, "Delegation denied: Agent present in revocation list"

        p_level = TRUST_LEVEL_HIERARCHY.get(parent_trust.upper(), 0)
        c_level = TRUST_LEVEL_HIERARCHY.get(child_trust.upper(), 0)

        if c_level > p_level:
            return False, f"Delegation narrowing violation: Child trust '{child_trust}' exceeds Parent trust '{parent_trust}'"

        return True, None
