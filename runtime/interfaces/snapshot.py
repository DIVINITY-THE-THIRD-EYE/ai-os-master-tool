from typing import Protocol


class ISnapshotEngine(Protocol):
    def create_snapshot(self, name: str) -> str: ...
