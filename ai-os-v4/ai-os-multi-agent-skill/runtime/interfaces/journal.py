from typing import Any, Dict, Protocol


class IJournalManager(Protocol):
    def log_operation(
        self, operation: str, entity_type: str, entity_id: str, payload: Dict[str, Any], workflow_id: str = None
    ) -> int: ...
    def mark_committed(self, sequence_no_up_to: int) -> None: ...
