from typing import Protocol, TypeVar, Optional, cast

T = TypeVar('T')
R = TypeVar('R')
E = TypeVar('E', bound=BaseException)

class ThFunction(Protocol[T, R, E]):
    def apply(self, t: T) -> R:
        """
        Применяет функцию к аргументу t.
        Может выбрасывать исключение типа E.
        """
        ...

def unchecked(function: Optional[ThFunction[T, R, E]]) -> Optional[ThFunction[T, R, Exception]]:
    """
    Возвращает данную ThFunction, приведённую к варианту с исключением типа Exception,
    либо None, если function равен None.
    """
    return cast(Optional[ThFunction[T, R, Exception]], function)
