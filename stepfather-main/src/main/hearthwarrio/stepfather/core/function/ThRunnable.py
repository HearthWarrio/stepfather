from typing import Protocol, TypeVar, Optional, cast

E = TypeVar('E', bound=BaseException)

class ThRunnable(Protocol[E]):
    def run(self) -> None:
        """
        Performs this operation.
        May throw an exception of type E.
        """
        ...

def unchecked(runnable: Optional[ThRunnable[E]]) -> Optional[ThRunnable[Exception]]:
    """
    Returns the given ThRunnable as unchecked (i.e. with exception type Exception)
    or None if runnable is None.
    """
    return cast(Optional[ThRunnable[Exception]], runnable)