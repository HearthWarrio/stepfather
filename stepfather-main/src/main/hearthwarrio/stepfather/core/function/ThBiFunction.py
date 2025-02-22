from typing import Protocol, TypeVar, Optional, cast

T = TypeVar('T')
U = TypeVar('U')
R = TypeVar('R')
E = TypeVar('E', bound=BaseException)

class ThBiFunction(Protocol[T, U, R, E]):
    def apply(self, t: T, u: U) -> R:
        """
        Applies this function to the given arguments.
        May throw an exception of type E.
        """
        ...

def unchecked(function: Optional[ThBiFunction[T, U, R, E]]) -> Optional[ThBiFunction[T, U, R, Exception]]:
    """
    Returns the given ThBiFunction as unchecked (i.e. with exception type Exception)
    or None if function is None.
    """
    return cast(Optional[ThBiFunction[T, U, R, Exception]], function)