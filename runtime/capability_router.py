"""
AI OS Capability Router — routes tasks to agents based on capability matching.

Implements routing rules from capability_registry.yaml:
1. Match task capability requirement to registered capability
2. Select agent with READY status and highest performance_score
3. Apply load balancing across agents providing same capability
4. Fall back to next available agent if primary is unhealthy
5. Escalate to orchestrator if no agent available

FIX: Added threading.Lock for thread-safe round-robin counters.
"""

import logging
import threading
from typing import Dict, List, Optional, Tuple

from .agent_registry import AgentRecord, AgentRegistry

logger = logging.getLogger("ai_os.capability_router")


class CapabilityRouter:
    """
    Routes capability requests to available agents.

    All routing is capability-driven. The router enforces:
    - deny_by_default: capabilities not registered are rejected
    - least_privilege: routing respects agent permission boundaries
    - health-first: only healthy agents receive assignments
    - thread-safe: round-robin counters protected by Lock
    """

    def __init__(self, registry: AgentRegistry):
        self._registry = registry
        self._round_robin_counters: Dict[str, int] = {}
        self._counter_lock = threading.Lock()   # FIX: thread-safe counters
        logger.info("CapabilityRouter initialized")

    def route(
        self,
        capability: str,
        task_id: str,
        trace_id: str,
        preferred_agent_id: Optional[str] = None,
    ) -> Optional[AgentRecord]:
        """
        Route a capability request to an available agent.

        Returns the selected AgentRecord, or None if escalation required.
        """
        candidates = self._registry.find_by_capability(capability)

        if not candidates:
            logger.warning(
                f"No available agents for capability '{capability}' "
                f"(task={task_id}, trace={trace_id}). Escalate to orchestrator."
            )
            return None

        # If preferred agent is available, use it
        if preferred_agent_id:
            preferred = next(
                (a for a in candidates if a.agent_id == preferred_agent_id),
                None
            )
            if preferred:
                logger.info(
                    f"Routing capability '{capability}' to preferred agent "
                    f"'{preferred_agent_id}' (task={task_id})"
                )
                return preferred

        # Thread-safe load-balance using round-robin within capability group
        with self._counter_lock:
            counter = self._round_robin_counters.get(capability, 0)
            selected = candidates[counter % len(candidates)]
            self._round_robin_counters[capability] = counter + 1

        logger.info(
            f"Routing capability '{capability}' to agent '{selected.agent_id}' "
            f"(performance={selected.performance_score:.2f}, task={task_id})"
        )
        return selected

    def can_route(self, capability: str) -> bool:
        """Check if any healthy agent is available for the given capability."""
        return len(self._registry.find_by_capability(capability)) > 0

    def get_routing_plan(
        self, required_capabilities: List[str]
    ) -> Tuple[Dict[str, Optional[str]], List[str]]:
        """
        Plan routing for a set of required capabilities.

        Returns:
            - routing_plan: {capability -> agent_id or None}
            - missing: capabilities with no available agent
        """
        routing_plan: Dict[str, Optional[str]] = {}
        missing: List[str] = []

        for cap in required_capabilities:
            candidates = self._registry.find_by_capability(cap)
            if candidates:
                routing_plan[cap] = candidates[0].agent_id
            else:
                routing_plan[cap] = None
                missing.append(cap)

        if missing:
            logger.warning(
                f"Routing plan incomplete. No agents for: {missing}"
            )

        return routing_plan, missing
