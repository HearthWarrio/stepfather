from typing import Protocol, TypeVar, Optional, cast

T = TypeVar('T')
E = TypeVar('E', bound=BaseException)

class ThConsumer(Protocol[T, E]):
    def accept(self, t: T) -> None:
        """
        Performs this operation on the given argument.
        May throw an exception of type E.
        """
        ...

def unchecked(consumer: Optional[ThConsumer[T, E]]) -> Optional[ThConsumer[T, Exception]]:
    """
    Returns the given ThConsumer as unchecked (i.e. with exception type Exception)
    or None if consumer is None.
    """
    return cast(Optional[ThConsumer[T, Exception]], consumer)