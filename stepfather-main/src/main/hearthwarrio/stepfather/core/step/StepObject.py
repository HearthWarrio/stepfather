from typing import Any, Optional, Protocol

class StepObject(Protocol):
    def with_artifact(self, name: str, value: Any) -> "StepObject":
        """
        Возвращает step object с заданным артефактом.
        Может выбрасывать StepfatherException, если value равен None.
        """
        ...

    def artifact(self, name: str) -> Optional[Any]:
        """
        Возвращает артефакт по имени.
        Может выбрасывать StepfatherException, если name равен None.
        """
        ...
