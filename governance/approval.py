"""
AIOS Cryptographic Human Approval Engine.
Generates and verifies tamper-evident cryptographic approval artifacts.
"""

import hmac
import hashlib
import json
import time
import uuid
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class CryptographicApprovalArtifact(BaseModel):
    approval_id: str
    task_id: str
    artifact_hash: str
    approver_id: str
    timestamp: float = Field(default_factory=time.time)
    signature: str


class CryptographicApprovalEngine:
    """
    HMAC-SHA256 Cryptographic Approval Engine.
    Produces tamper-evident approval signatures for tasks and artifact hashes.
    """

    def __init__(self, secret_key: bytes = b"AIOS_MASTER_GOVERNANCE_SECRET_KEY"):
        self.secret_key = secret_key

    def _compute_signature(self, approval_id: str, task_id: str, artifact_hash: str, approver_id: str, timestamp: float) -> str:
        payload = f"{approval_id}:{task_id}:{artifact_hash}:{approver_id}:{timestamp}"
        return hmac.new(self.secret_key, payload.encode("utf-8"), hashlib.sha256).hexdigest()

    def create_signed_approval(self, task_id: str, artifact_hash: str, approver_id: str = "HUMAN_A13") -> CryptographicApprovalArtifact:
        approval_id = f"APPR-{str(uuid.uuid4())[:8].upper()}"
        now = time.time()
        sig = self._compute_signature(approval_id, task_id, artifact_hash, approver_id, now)
        
        return CryptographicApprovalArtifact(
            approval_id=approval_id,
            task_id=task_id,
            artifact_hash=artifact_hash,
            approver_id=approver_id,
            timestamp=now,
            signature=sig
        )

    def verify_approval(self, artifact: CryptographicApprovalArtifact, expected_artifact_hash: str) -> bool:
        if artifact.artifact_hash != expected_artifact_hash:
            return False
            
        expected_sig = self._compute_signature(
            artifact.approval_id,
            artifact.task_id,
            artifact.artifact_hash,
            artifact.approver_id,
            artifact.timestamp
        )
        
        return hmac.compare_digest(artifact.signature, expected_sig)
