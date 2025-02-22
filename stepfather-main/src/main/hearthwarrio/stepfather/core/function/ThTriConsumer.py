from typing import Protocol, TypeVar, Optional, cast

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')
E = TypeVar('E', bound=BaseException)

class ThTriConsumer(Protocol[T, U, V, E]):
    def accept(self, t: T, u: U, v: V) -> None:
        """
        Performs this operation on the given arguments.
        May throw an exception of type E.
        """
        ...

def unchecked(consumer: Optional[ThTriConsumer[T, U, V, E]]) -> Optional[ThTriConsumer[T, U, V, Exception]]:
    """
    Returns the given ThTriConsumer as unchecked (i.e. with exception type Exception)
    or None if consumer is None.
    """
    return cast(Optional[ThTriConsumer[T, U, V, Exception]], consumer)