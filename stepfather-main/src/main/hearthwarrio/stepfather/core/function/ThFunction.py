from typing import Protocol, TypeVar, Optional

T = TypeVar('T')
R = TypeVar('R')

class ThFunction(Protocol[T, R]):
    def apply(self, t: T) -> R:
        """
        Применяет функцию к данному аргументу.
        Может выбрасывать исключение.
        """
        ...

def unchecked(function: Optional[ThFunction[T, R]]) -> Optional[ThFunction[T, R]]:
    """
    Возвращает переданную ThFunction в "unchecked" виде или None, если function равен None.
    """
    return function
