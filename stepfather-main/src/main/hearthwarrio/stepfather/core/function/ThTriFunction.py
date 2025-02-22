from typing import Protocol, TypeVar, Optional, cast

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')
R = TypeVar('R')
E = TypeVar('E', bound=BaseException)

class ThTriFunction(Protocol[T, U, V, R, E]):
    def apply(self, t: T, u: U, v: V) -> R:
        """
        Applies this function to the given arguments.
        May raise an exception of type E.
        """
        ...

def unchecked(function: Optional[ThTriFunction[T, U, V, R, E]]) -> Optional[ThTriFunction[T, U, V, R, Exception]]:
    """
    Returns the given ThTriFunction as unchecked (i.e. with exception type Exception)
    or None if function is None.
    """
    return cast(Optional[ThTriFunction[T, U, V, R, Exception]], function)