from typing import Protocol


class IRecoveryManager(Protocol):
    def heal(self) -> bool: ...
