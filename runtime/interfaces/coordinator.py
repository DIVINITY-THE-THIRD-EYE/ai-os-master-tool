from typing import Any, Optional, Protocol


class IPersistenceCoordinator(Protocol):
    def flush(
        self, vram_conn: Optional[Any], current_image_version: int, is_dirty: bool, workflow_id: Optional[str] = None
    ) -> int: ...
