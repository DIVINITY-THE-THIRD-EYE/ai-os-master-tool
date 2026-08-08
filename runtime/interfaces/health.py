from typing import Any, Dict, Protocol


class IHealthMonitor(Protocol):
    def get_health_status(self, state_manager: Any) -> Dict[str, Any]: ...
