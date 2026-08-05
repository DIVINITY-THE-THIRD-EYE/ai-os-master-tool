"""
AI OS Agent Registry — dynamic registration and routing of agents.

Implements the agent_registry.yaml specification in Python.
All agents must register here before receiving task assignments.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

logger = logging.getLogger("ai_os.agent_registry")


@dataclass
class AgentRecord:
    """A registered agent in the AI OS Agent Registry."""
    agent_id: str
    name: str
    version: str
    capabilities: List[str]
    skills: List[str]
    tools: List[str]
    permissions: List[str]
    dependencies: List[str] = field(default_factory=list)
    status: str = "registered"           # created|registered|configured|ready|disabled|retired
    health_status: str = "unknown"       # healthy|degraded|unhealthy|unknown
    performance_score: float = 1.0       # 0.0-1.0
    availability: float = 1.0            # 0.0-1.0
    last_heartbeat: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def is_available(self) -> bool:
        return self.status == "ready" and self.health_status == "healthy"


class AgentRegistry:
    """
    Central registry of all AI OS agents.

    Routing strategy per capability_registry.yaml:
    1. Match by capability
    2. Filter by health status (healthy only)
    3. Load balance (round-robin)
    4. Fall back to performance score
    5. Escalate to orchestrator if none available
    """

    def __init__(self):
        self._agents: Dict[str, AgentRecord] = {}
        logger.info("AgentRegistry initialized")

    def register(self, agent: AgentRecord) -> None:
        """Register a new agent. Raises if agent_id already registered."""
        if agent.agent_id in self._agents:
            raise ValueError(
                f"Agent '{agent.agent_id}' is already registered. "
                "Use update_status to modify an existing agent."
            )
        agent.status = "registered"
        self._agents[agent.agent_id] = agent
        logger.info(f"Agent registered: {agent.agent_id} ({agent.name})")

    def configure(self, agent_id: str) -> None:
        """Mark agent as configured — configuration loaded from platform."""
        agent = self._get_or_raise(agent_id)
        agent.status = "configured"
        logger.info(f"Agent configured: {agent_id}")

    def mark_ready(self, agent_id: str) -> None:
        """Mark agent as ready to receive work assignments."""
        agent = self._get_or_raise(agent_id)
        if agent.status != "configured":
            raise ValueError(
                f"Agent must be 'configured' before marking ready. "
                f"Current status: {agent.status}"
            )
        agent.status = "ready"
        agent.health_status = "healthy"
        agent.last_heartbeat = datetime.now(timezone.utc).isoformat()
        logger.info(f"Agent ready: {agent_id}")

    def update_health(
        self,
        agent_id: str,
        health_status: str,
        availability: float,
        performance_score: Optional[float] = None,
    ) -> None:
        """Update agent health metrics from heartbeat."""
        agent = self._get_or_raise(agent_id)
        agent.health_status = health_status
        agent.availability = availability
        agent.last_heartbeat = datetime.now(timezone.utc).isoformat()
        if performance_score is not None:
            agent.performance_score = performance_score

    def disable(self, agent_id: str) -> None:
        """Disable agent — cannot receive assignments until re-enabled."""
        agent = self._get_or_raise(agent_id)
        agent.status = "disabled"
        logger.warning(f"Agent disabled: {agent_id}")

    def retire(self, agent_id: str) -> None:
        """Permanently retire agent from registry."""
        agent = self._get_or_raise(agent_id)
        agent.status = "retired"
        logger.info(f"Agent retired: {agent_id}")

    def find_by_capability(self, capability: str) -> List[AgentRecord]:
        """Return all ready, healthy agents providing the specified capability."""
        matches = [
            a for a in self._agents.values()
            if capability in a.capabilities and a.is_available()
        ]
        # Sort by performance score descending
        return sorted(matches, key=lambda a: a.performance_score, reverse=True)

    def get(self, agent_id: str) -> Optional[AgentRecord]:
        return self._agents.get(agent_id)

    def get_all_ready(self) -> List[AgentRecord]:
        return [a for a in self._agents.values() if a.is_available()]

    def list_all(self) -> List[AgentRecord]:
        return list(self._agents.values())

    def _get_or_raise(self, agent_id: str) -> AgentRecord:
        if agent_id not in self._agents:
            raise KeyError(f"Agent not found: {agent_id}")
        return self._agents[agent_id]
