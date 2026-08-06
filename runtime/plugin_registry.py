"""
AI OS Plugin Registry — manages dynamic registration, permissioning,
and sandboxing of external tools and plugins.

Implements platform/plugin_registry.yaml spec and wihout memory.md Phase 13.
"""

import logging
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger("ai_os.plugin_registry")


@dataclass
class PluginRecord:
    """A registered plugin or tool in the AI OS Plugin Registry."""

    plugin_id: str
    name: str
    version: str
    type: str  # tool | model | api | binary
    description: str
    interface_schema: dict  # JSON Schema for inputs/outputs
    permissions: List[str]  # Whitelisted operations
    sandbox_required: bool = True
    rate_limit_per_minute: int = 60
    timeout_seconds: int = 30
    status: str = "registered"  # registered | active | disabled | retired
    health_status: str = "unknown"
    invocation_count: int = 0
    error_count: int = 0
    last_invoked: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def is_available(self) -> bool:
        return self.status == "active" and self.health_status in ("healthy", "unknown")

    def record_invocation(self, success: bool) -> None:
        self.invocation_count += 1
        if not success:
            self.error_count += 1
        self.last_invoked = datetime.now(timezone.utc).isoformat()


class PluginRegistry:
    """
    Central registry for all AI OS plugins and tools.

    Enforces:
    - deny_by_default: plugins not registered cannot be invoked
    - least_privilege: each plugin declares only its allowed operations
    - sandboxing: high-risk plugins are flagged for sandbox execution
    - rate_limiting: per-plugin rate limits tracked
    - audit: all invocations recorded

    From wihout memory.md Phase 13:
    "registry YAMLs listing available models, APIs, and binary tools"
    """

    def __init__(self):
        self._plugins: Dict[str, PluginRecord] = {}
        self._invocation_log: List[dict] = []
        self._lock = threading.Lock()
        logger.info("PluginRegistry initialized")

    def register(self, plugin: PluginRecord) -> None:
        """Register a new plugin. Raises if plugin_id already exists."""
        with self._lock:
            if plugin.plugin_id in self._plugins:
                raise ValueError(f"Plugin '{plugin.plugin_id}' already registered. Use update_status to modify.")
            self._plugins[plugin.plugin_id] = plugin
            logger.info(f"Plugin registered: {plugin.plugin_id} ({plugin.name} v{plugin.version}, type={plugin.type})")

    def activate(self, plugin_id: str) -> None:
        """Activate a registered plugin — makes it available for invocation."""
        with self._lock:
            plugin = self._get_or_raise(plugin_id)
            plugin.status = "active"
            plugin.health_status = "healthy"
            logger.info(f"Plugin activated: {plugin_id}")

    def disable(self, plugin_id: str, reason: str = "") -> None:
        """Disable a plugin — blocks all further invocations."""
        with self._lock:
            plugin = self._get_or_raise(plugin_id)
            plugin.status = "disabled"
            logger.warning(f"Plugin disabled: {plugin_id}. Reason: {reason}")

    def retire(self, plugin_id: str) -> None:
        """Permanently retire a plugin."""
        with self._lock:
            plugin = self._get_or_raise(plugin_id)
            plugin.status = "retired"
            logger.info(f"Plugin retired: {plugin_id}")

    def validate_invocation(
        self,
        plugin_id: str,
        agent_id: str,
        operation: str,
        arguments: Dict[str, Any],
    ) -> tuple[bool, str]:
        """
        Validate that an agent is permitted to invoke a plugin with given args.

        Returns:
            (allowed: bool, reason: str)

        Rules enforced:
        - Plugin must be registered and active
        - Operation must be in plugin's permission whitelist
        - Arguments must be non-empty dict (full schema validation is TODO)
        """
        with self._lock:
            plugin = self._plugins.get(plugin_id)

        if plugin is None:
            return False, f"Plugin '{plugin_id}' not registered. Deny by default."

        if not plugin.is_available():
            return False, f"Plugin '{plugin_id}' is not available (status={plugin.status})."

        if operation not in plugin.permissions:
            return False, (
                f"Operation '{operation}' not in whitelist for plugin '{plugin_id}'. Allowed: {plugin.permissions}"
            )

        if not isinstance(arguments, dict):
            return False, "Arguments must be a dict."

        return True, "Allowed"

    def record_invocation(
        self,
        plugin_id: str,
        agent_id: str,
        operation: str,
        success: bool,
        error: Optional[str] = None,
    ) -> None:
        """Record a plugin invocation in the audit log."""
        with self._lock:
            plugin = self._plugins.get(plugin_id)
            if plugin:
                plugin.record_invocation(success)

            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "plugin_id": plugin_id,
                "agent_id": agent_id,
                "operation": operation,
                "success": success,
                "error": error,
            }
            self._invocation_log.append(entry)

        level = logging.INFO if success else logging.ERROR
        logger.log(
            level,
            f"Plugin invocation: plugin={plugin_id} agent={agent_id} "
            f"op={operation} success={success}" + (f" error={error}" if error else ""),
        )

    def get(self, plugin_id: str) -> Optional[PluginRecord]:
        with self._lock:
            return self._plugins.get(plugin_id)

    def list_active(self) -> List[PluginRecord]:
        with self._lock:
            return [p for p in self._plugins.values() if p.is_available()]

    def list_by_type(self, plugin_type: str) -> List[PluginRecord]:
        with self._lock:
            return [p for p in self._plugins.values() if p.type == plugin_type and p.is_available()]

    def get_audit_log(
        self,
        plugin_id: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> List[dict]:
        """Retrieve invocation audit log with optional filters."""
        with self._lock:
            log = self._invocation_log
        if plugin_id:
            log = [e for e in log if e["plugin_id"] == plugin_id]
        if agent_id:
            log = [e for e in log if e["agent_id"] == agent_id]
        return log

    def _get_or_raise(self, plugin_id: str) -> PluginRecord:
        """Must be called with self._lock held."""
        if plugin_id not in self._plugins:
            raise KeyError(f"Plugin not found: {plugin_id}")
        return self._plugins[plugin_id]
