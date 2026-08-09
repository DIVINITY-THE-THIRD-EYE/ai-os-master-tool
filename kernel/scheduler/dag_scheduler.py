"""
AIOS Secure DAG Scheduler — Enforces mandatory cryptographic human approval signatures for High/Critical risk tasks.
Raises SecurityViolationError if approval signature is missing or tampered with.
"""

from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field
from security.contracts import RiskLevel
from governance.approval import CryptographicApprovalArtifact, CryptographicApprovalEngine


class SecurityViolationError(Exception):
    """Raised when a security policy or required cryptographic approval gate is violated."""
    pass


class DAGTaskNode(BaseModel):
    node_id: str
    task_id: str
    risk_level: RiskLevel = RiskLevel.LOW
    dependencies: Set[str] = Field(default_factory=set)
    artifact_hash: str = ""
    executed: bool = False


class SecureDAGScheduler:
    def __init__(self, approval_engine: Optional[CryptographicApprovalEngine] = None):
        self.nodes: Dict[str, DAGTaskNode] = {}
        self.approval_artifacts: Dict[str, CryptographicApprovalArtifact] = {}
        self.approval_engine = approval_engine or CryptographicApprovalEngine()

    def register_node(self, node: DAGTaskNode) -> None:
        self.nodes[node.node_id] = node

    def submit_approval_artifact(self, artifact: CryptographicApprovalArtifact) -> None:
        self.approval_artifacts[artifact.task_id] = artifact

    def can_execute_node(self, node_id: str) -> bool:
        node = self.nodes.get(node_id)
        if not node:
            return False

        # 1. Verify dependencies executed
        for dep_id in node.dependencies:
            dep_node = self.nodes.get(dep_id)
            if not dep_node or not dep_node.executed:
                return False

        # 2. Strict High/Critical Risk Cryptographic Approval Enforcement
        if node.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            approval_artifact = self.approval_artifacts.get(node.task_id)
            if not approval_artifact:
                raise SecurityViolationError(
                    f"Security Gate Violation: High/Critical risk node '{node_id}' (task '{node.task_id}') lacks mandatory cryptographic human approval artifact."
                )

            if not self.approval_engine.verify_approval(approval_artifact, node.artifact_hash):
                raise SecurityViolationError(
                    f"Security Gate Violation: Cryptographic signature verification failed for node '{node_id}' (task '{node.task_id}'). Artifact tampered or invalid."
                )

        return True

    def execute_node(self, node_id: str) -> None:
        if not self.can_execute_node(node_id):
            raise RuntimeError(f"Cannot execute node '{node_id}': dependencies not met.")
        self.nodes[node_id].executed = True
