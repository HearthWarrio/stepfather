from typing import Protocol, TypeVar
from src.main.hearthwarrio.stepfather.core.sc.base import StepContext

P = TypeVar('P', bound=StepContext)
F = TypeVar('F', bound=StepContext)

class MemSC(Protocol[P, F]):
    def previous(self) -> P:
        """
        Возвращает предыдущий step context.
        """
        ...

    def forget(self) -> F:
        """
        Возвращает non-memorizing step context.
        """
        ...